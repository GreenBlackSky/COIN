"""Flask blueprint, that contains accounts manipulation methods."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .constants import MAX_ACCOUNTS, STARTING_CATEGORIES
from .model import (
    session,
    UserModel,
    AccountModel,
    AccountSchema,
    CategoryModel,
    SavePointModel,
)
from .user import authorized_user


router = APIRouter()


def create_account(user_id, name):
    """Create new account."""
    account = AccountModel(
        user_id=user_id,
        name=name,
    )
    session.add(account)
    session.commit()

    categories = [
        CategoryModel(user_id=user_id, account_id=account.id, **category)
        for category in STARTING_CATEGORIES
    ]
    session.add_all(categories)
    session.commit()
    return account


class CreateAccountRequest(BaseModel):
    name: str


@router.post("/create_account")  # PUT
def create_account_endpoint(
    request: CreateAccountRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Request creating new account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id
    )
    if accounts.count() >= MAX_ACCOUNTS:
        return {"status": "max accounts"}
    if (
        session.query(AccountModel)
        .filter(
            AccountModel.user_id == current_user.id,
            AccountModel.name == request.name,
        )
        .first()
    ):
        return {"status": "account already exists"}
    return {
        "status": "OK",
        "account": AccountSchema.from_orm(
            create_account(current_user.id, request.name)
        ).dict(),
    }


def get_account(account_id: int) -> dict | None:
    """Get all users accounts."""
    if account := session.query(AccountModel).get(account_id):
        return AccountSchema.from_orm(account).dict()


def get_accounts(user_id: int):
    """Get all users accounts."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id
    )
    return [
        AccountSchema.from_orm(account).dict() for account in accounts.all()
    ]


@router.post("/get_accounts")
def get_accounts_endpoint(current_user: UserModel = Depends(authorized_user)):
    """Web endpoint for getting accounts of user."""
    return {
        "status": "OK",
        "accounts": get_accounts(current_user.id),
    }


class EditAccountRequest(BaseModel):
    id: int
    name: str


@router.post("/edit_account")
def edit_account(
    request: EditAccountRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Request to edit account."""
    account = session.get(AccountModel, request.id)
    if account is None:
        return {"status": "no such account"}

    if account.user_id != current_user.id:
        return {"status": "accessing account of another user"}

    if (
        session.query(AccountModel)
        .filter(
            AccountModel.user_id == current_user.id,
            AccountModel.name == request.name,
            AccountModel.id != request.id,
        )
        .count()
        != 0
    ):
        return {"status": "account already exists"}

    account.name = request.name
    session.commit()
    return {"status": "OK", "account": AccountSchema.from_orm(account).dict()}


class DeleteAccountRequest(BaseModel):
    account_id: int


@router.post("/delete_account")
def delete_account(
    request: DeleteAccountRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Delete existing account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
    )
    if accounts.count() == 1:
        return {"status": "can't delete the only account"}

    account = session.get(AccountModel, request.account_id)
    if account is None:
        return {"status": "no such account"}

    if account.user_id != current_user.id:
        return {"status": "accessing account of another user"}

    session.query(SavePointModel).filter(
        SavePointModel.account_id == account.id
    ).delete()
    session.delete(account)
    session.commit()
    return {"status": "OK", "account": AccountSchema.from_orm(account).dict()}
