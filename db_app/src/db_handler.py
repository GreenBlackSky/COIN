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
    def create_user(self, name, password_hash):
        """Create new User record in db."""
        user = self.db.query(UserModel).filter_by(name=name).first()
        if user:
            return None
        user = UserModel(name=name, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        return user

    @log_method
    def get_user(self, user_id=None, name=None):
        """Get user by id or by name."""
        if user_id:
            user = self.db.query(UserModel).get(user_id)
        elif name:
            user = self.db.query(UserModel).filter_by(name=name).first()
        else:
            raise Exception("Man, either id or name!")
        return user

    @log_method
    def update_user(self, user_id, name, password_hash):
        """Update user data in db."""
        user = self.db.query(UserModel).get(user_id)
        if user is None:
            return None
        user.name = name
        if password_hash is not None:
            user.password_hash = password_hash
        self.db.commit()
        return user

    @log_method
    def create_account(self, user_id, account_name):
        """Create new Account record in db."""
        if self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.name == account_name
        ).first():
            return None
        account = AccountModel(
            user_id=user_id,
            name=account_name,
            actual_date=dateTools.today(),
            balance=0
        )
        self.db.add(account)
        self.db.commit()
        return account

    @log_method
    def get_accounts(self, user_id):
        """Get account from db by id."""
        accounts = self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id
        )
        if accounts.count() == 0:
            return None
        return accounts.all()

    @log_method
    def create_starting_labels(self, account_id):
        pass

    @log_method
    def get_labels(self, account_id):
        pass

    @log_method
    def get_templates(self, account_id):
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
