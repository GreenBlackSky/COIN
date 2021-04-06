"""Handle connection to database."""

from datetime import date as dateTools, time

from common.debug_tools import log_method
from .models import session, UserModel, AccountModel, DateModel


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
    def update_user(self, user_id, email, password_hash, commit=False):
        """Update user data in db."""
        user = self.db.query(UserModel).get(user_id)
        if user is None:
            return None
        user.email = email
        if password_hash is not None:
            user.password_hash = password_hash
        if commit:
            self.db.commit()
        return user

    @log_method
    def create_account(self, user_id, is_main=False, commit=True):
        """Create new Account record in db."""
        account = AccountModel(user_id=user_id, is_main=is_main)
        self.db.add(account)
        if commit:
            self.db.commit()
        # self.create_date(account.id, dateTools.today(), 0, 0, True)
        return account

    # @log_method
    # def get_account(self, account_id):
    #     """Get account from db by id."""
    #     return self.db.query(AccountModel).get(account_id)

    @log_method
    def clear(self):
        """Clear database."""
        date_count = self.db.query(DateModel).delete()
        account_count = self.db.query(AccountModel).delete()
        user_count = self.db.query(UserModel).delete()
        self.db.commit()
        return {
            'user': user_count,
            'account': account_count,
            'date': date_count
        }
