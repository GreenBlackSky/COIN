"""Handle connection to database."""

from datetime import date as dateTools, time, datetime
from typing import List, Optional

from common.debug_tools import log_method

from .models import session, CategoryModel, TemplateModel, \
    UserModel, AccountModel


class DBHandler:
    """Handle reading from and writing to database."""

    db = session

    @log_method
    def create_user(self, email, password_hash):
        """Create new User record in db."""
        user = self.db.query(UserModel).filter_by(email=email).first()
        if user:
            return None
        user = UserModel(email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        return user

    @log_method
    def get_user(self, user_id=None, email=None):
        """Get user by id or by email."""
        if user_id:
            user = self.db.query(UserModel).get(user_id)
        elif email:
            user = self.db.query(UserModel).filter_by(email=email).first()
        else:
            raise Exception("Man, either id or email!")
        return user

    @log_method
    def update_user(self, user_id, email, password_hash):
        """Update user data in db."""
        user = self.db.query(UserModel).get(user_id)
        if user is None:
            return None
        user.email = email
        if password_hash is not None:
            user.password_hash = password_hash
        self.db.commit()
        return user

    @log_method
    def create_account(self, user_id, account_name, is_main=False):
        """Create new Account record in db."""
        account = self.db.query(AccountModel).filter(
            user_id == user_id,
            account_name == account_name
        ).first()
        if account:
            return None
        account = AccountModel(
            user_id=user_id,
            name=account_name,
            actual_date=dateTools.today(),
            balance=0,
            unconfirmed_balance=0,
            is_main=is_main
        )
        self.db.add(account)
        self.db.commit()
        return account

    @log_method
    def get_accounts(self, user_id) -> Optional[UserModel]:
        """Get account from db by id."""
        return self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id
        )

    @log_method
    def create_starting_categories(self, account_id) -> List[CategoryModel]:
        pass

    @log_method
    def get_categories(self, account_id) -> List[CategoryModel]:
        pass

    @log_method
    def get_templates(self, account_id) -> TemplateModel:
        pass

    @log_method
    def create_starting_templates(self, account_id):
        pass

    @log_method
    def clear(self):
        """Clear database."""
        account_count = self.db.query(AccountModel).delete()
        user_count = self.db.query(UserModel).delete()
        self.db.commit()
        return {
            'user': user_count,
            'account': account_count,
        }
