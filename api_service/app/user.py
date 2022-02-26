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
from .model import AccountModel, CategoryModel, session, UserModel, UserSchema


router = APIRouter()


def authorized_user(Authorize: AuthJWT = Depends()) -> UserModel:
    Authorize.jwt_required()
    name = Authorize.get_jwt_subject()
    return session.query(UserModel).filter(UserModel.name == name).first()


class UserRequest(BaseModel):
    name: str
    password: str


@router.post("/register")
def register(user_data: UserRequest, Authorize: AuthJWT = Depends()):
    """Register new user."""
    if Authorize.get_jwt_subject():
        return {"status": "already authorized"}

    user = session.query(UserModel).filter_by(name=user_data.name).first()
    if user:
        return {"status": "user exists"}

    password_hash = md5(user_data.password.encode()).hexdigest()
    user = UserModel(name=user_data.name, password_hash=password_hash)
    session.add(user)
    session.commit()
    account = AccountModel(user_id=user.id, name=MAIN_ACCOUNT_NAME)
    session.add(account)
    session.commit()
    for starting_category in STARTING_CATEGORIES:
        category = CategoryModel(
            account_id=account.id, user_id=user.id, **starting_category
        )
        session.add(category)
    session.commit()
    return {
        "access_token": Authorize.create_access_token(subject=user_data.name),
        "status": "OK",
        "user": UserSchema.from_orm(user).dict(),
    }


@router.post("/login")
def login(user_data: UserRequest, Authorize: AuthJWT = Depends()):
    """Log in user."""
    user = session.query(UserModel).filter_by(name=user_data.name).first()
    if user is None:
        return {"status": "no such user"}, 401

    if user.password_hash != md5(user_data.password.encode()).hexdigest():
        return {"status": "wrong password"}, 401

    return {
        "status": "OK",
        "user": UserSchema.from_orm(user).dict(),
        "access_token": Authorize.create_access_token(subject=user_data.name),
    }


class EditUserRequest(BaseModel):
    name: str
    old_pass: str
    new_pass: str


@router.post("/edit_user")
def edit_user(user_data: EditUserRequest, Authorize: AuthJWT = Depends()):
    """Edit user."""
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    if user_data.name != current_user.name:
        other_user = (
            session.query(UserModel).filter_by(name=user_data.name).first()
        )
        if other_user:
            return {"status": "user exists"}
    current_user.name = user_data.name

    got_old_pass = user_data.old_pass is not None
    got_new_pass = user_data.new_pass is not None
    if got_new_pass != got_old_pass:
        return {
            "status": "new password must be provided with an old password"
        }, 412

    if got_old_pass and got_new_pass:
        old_hash = md5(user_data.old_pass.encode()).hexdigest()
        if old_hash != current_user.password_hash:
            return {"status": "wrong password"}, 401
        new_hash = md5(user_data.new_pass.encode()).hexdigest()
        current_user.password_hash = new_hash

    session.commit()
    return {"status": "OK", "user": UserSchema.from_orm(current_user).dict()}


@router.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    """Log out user."""
    Authorize.jwt_required()

    return {"status": "OK"}
