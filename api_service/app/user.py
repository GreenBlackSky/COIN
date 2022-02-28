"""
User logic stuff.

This module contains methods to create new user or
to get access to existing one.
"""

from hashlib import md5

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


from .constants import MAIN_ACCOUNT_NAME, STARTING_CATEGORIES
from .exceptions import LogicException
from .model import (
    CategoryModel,
    create_account_entry,
    session,
    UserModel,
    UserSchema,
    create_account,
)


router = APIRouter()


def authorized_user(Authorize: AuthJWT = Depends()) -> UserModel:
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return session.query(UserModel).get(user_id)


class UserRequest(BaseModel):
    name: str
    password: str


@router.post("/register")
def register(user_data: UserRequest, Authorize: AuthJWT = Depends()):
    """Register new user."""
    if Authorize.get_jwt_subject():
        raise LogicException("already authorized")

    user = session.query(UserModel).filter_by(name=user_data.name).first()
    if user:
        raise LogicException("user exists")

    password_hash = md5(user_data.password.encode()).hexdigest()
    user = UserModel(name=user_data.name, password_hash=password_hash)
    session.add(user)
    session.commit()
    account = create_account(user_id=user.id, name=MAIN_ACCOUNT_NAME)
    session.add(account)
    session.commit()
    for starting_category in STARTING_CATEGORIES:
        category = create_account_entry(
            CategoryModel,
            user_id=user.id,
            account_id=account.id,
            **starting_category
        )
        session.add(category)
    session.commit()
    return {
        "access_token": Authorize.create_access_token(subject=user.id),
        "status": "OK",
        "user": UserSchema.from_orm(user).dict(),
    }


@router.post("/login")
def login(user_data: UserRequest, Authorize: AuthJWT = Depends()):
    """Log in user."""
    user = session.query(UserModel).filter_by(name=user_data.name).first()
    if user is None:
        raise LogicException("no such user")
    if user.password_hash != md5(user_data.password.encode()).hexdigest():
        raise LogicException("wrong password")
    return {
        "status": "OK",
        "user": UserSchema.from_orm(user).dict(),
        "access_token": Authorize.create_access_token(subject=user.id),
    }


@router.post("/get_user_data")
def get_user_data(user: UserModel = Depends(authorized_user)):
    return {"status": "OK", "user": UserSchema.from_orm(user).dict()}


class EditUserRequest(BaseModel):
    name: str
    old_pass: str
    new_pass: str


@router.post("/edit_user")
def edit_user(
    user_data: EditUserRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Edit user."""
    if user_data.name != current_user.name:
        other_user = (
            session.query(UserModel).filter_by(name=user_data.name).first()
        )
        if other_user:
            raise LogicException("user exists")
    current_user.name = user_data.name

    got_old_pass = user_data.old_pass is not None
    got_new_pass = user_data.new_pass is not None
    if got_new_pass != got_old_pass:
        raise LogicException(
            "new password must be provided with an old password"
        )
    if got_old_pass and got_new_pass:
        old_hash = md5(user_data.old_pass.encode()).hexdigest()
        if old_hash != current_user.password_hash:
            raise LogicException("wrong password")
        new_hash = md5(user_data.new_pass.encode()).hexdigest()
        current_user.password_hash = new_hash

    session.commit()
    return {"status": "OK", "user": UserSchema.from_orm(current_user).dict()}


@router.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    """Log out user."""
    Authorize.jwt_required()

    return {"status": "OK"}
