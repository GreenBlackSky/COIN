"""Flask blueprint, that contains accounts manipulation methods."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .utils.constants import MAX_ACCOUNTS, STARTING_CATEGORIES
from .utils.exceptions import LogicException
from .utils.models import (
    create_account as create_account_impl,
    create_account_entry,
    UserModel,
    AccountModel,
    CategoryModel,
    SavePointModel,
)
from .user import authorized_user
from .category import delete_category
from .utils.database import get_session


router = APIRouter()


async def create_account(session: AsyncSession, user_id, name):
    """Create new account."""
    account = await create_account_impl(session, user_id, name)
    session.add(account)
    await session.commit()

    categories = [
        await create_account_entry(
            session,
            CategoryModel,
            user_id=user_id,
            account_id=account.id,
            **category
        )
        for category in STARTING_CATEGORIES
    ]
    session.add_all(categories)
    await session.commit()
    return account


class CreateAccountRequest(BaseModel):
    name: str


@router.post("/create_account")  # POST
async def create_account_endpoint(
    request: CreateAccountRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request creating new account."""
    session: AsyncSession
    async with async_session() as session:
        query = await session.execute(
            select(AccountModel).where(AccountModel.user_id == current_user.id)
        )
        if len(query.all()) >= MAX_ACCOUNTS:
            raise LogicException("max accounts")
        query = await session.execute(
            select(AccountModel)
            .where(AccountModel.user_id == current_user.id)
            .where(AccountModel.name == request.name)
        )
        if query.first():
            raise LogicException("account already exists")
        account = await create_account(session, current_user.id, request.name)
    return {
        "status": "OK",
        "account": account.to_dict(),
    }


@router.post("/get_accounts")
async def get_accounts_endpoint(
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get all users accounts."""
    session: AsyncSession
    async with async_session() as session:
        query = await session.execute(
            select(AccountModel).where(AccountModel.user_id == current_user.id)
        )
    return {
        "status": "OK",
        "accounts": [account.to_dict() for (account,) in query.all()],
    }


class EditAccountRequest(BaseModel):
    account_id: int
    name: str


@router.post("/edit_account")
async def edit_account(
    request: EditAccountRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request to edit account."""
    session: AsyncSession
    async with async_session() as session:
        account = await session.get(
            AccountModel, (current_user.id, request.account_id)
        )
        if not account:
            raise LogicException("no such account")

        query = await session.execute(
            select(AccountModel)
            .where(AccountModel.user_id == current_user.id)
            .where(AccountModel.name == request.name)
            .where(AccountModel.id != request.account_id)
        )
        if len(query.all()) != 0:
            raise LogicException("account already exists")

        account.name = request.name
        await session.commit()
    return {"status": "OK", "account": account.to_dict()}


class DeleteAccountRequest(BaseModel):
    account_id: int


@router.post("/delete_account")
async def delete_account(
    request: DeleteAccountRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Delete existing account."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            query = await session.execute(
                select(AccountModel).where(
                    AccountModel.user_id == current_user.id
                )
            )
            if len(query.all()) == 1:
                raise LogicException("can't delete the only account")

            account = await session.get(
                AccountModel, (current_user.id, request.account_id)
            )
            if account is None:
                raise LogicException("no such account")

            await session.execute(
                delete(SavePointModel).where(
                    SavePointModel.account_id == account.id
                )
            )
            await session.delete(account)
            query = await session.execute(
                select(CategoryModel)
                .where(CategoryModel.user_id == current_user.id)
                .where(CategoryModel.account_id == account.id)
            )
            for (category,) in query.all():
                await delete_category(
                    session, current_user.id, account.id, category.id
                )

    return {"status": "OK", "account": account.to_dict()}
