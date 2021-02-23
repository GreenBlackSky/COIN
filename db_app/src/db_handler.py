"""Handle connection to database."""

from datetime import date as dateTools, time

from common.debug_tools import log_method
from .models import session, TestData, UserModel, AccountModel, DateModel


class DBHandler:
    """Handle connection to database."""

    db = session

    @log_method
    def create_user(self, name, password_hash):
        user = self.db.query(UserModel).filter_by(name=name).first()
        if user:
            return None
        user = UserModel(name=name, password_hash=password_hash)
        self.db.add(user)
        account = self.create_account(user.id, name, commit=False)
        dateEnt = self.create_date(account.id, True, dateTools.today(), 0, 0, commit=False)
        self.db.commit()
        return user, account, dateEnt

    @log_method
    def create_account(self, user_id, name, commit=True):
        account = AccountModel(user_id=user_id, name=name)
        self.db.add(account)
        if commit:
            self.db.commit()
        return account

    @log_method
    def create_date(self, account_id, is_actual, date, balance, unconfirmed_balance, commit=True):
        dateEnt = DateModel(
            account_id=account_id,
            is_actual=is_actual,
            date=date,
            balance=balance,
            unconfirmed_balance=unconfirmed_balance
        )
        self.db.add(dateEnt)
        if commit:
            self.db.commit()
        return dateEnt

    @log_method
    def get_user(self, user_id=None, name=None):
        """Get user by id or by name."""
        if user_id:
            user = self.db.query(UserModel).get(user_id)
        elif name:
            user = self.db.query(UserModel).filter_by(name=name).first()
        else:
            raise Exception("Man, either id or name!")
        if user is None:
            return None
        return user

    @log_method
    def get_account(self):
        pass

    @log_method
    def edit_account(self):
        pass

    @log_method
    def delete_account(self):
        pass

    @log_method
    def test_set_value(self, value):
        data = TestData(value=value)
        self.db.add(data)
        self.db.commit()
        return data.id

    @log_method
    def test_get_value(self, data_id):
        data = self.db.query(TestData).get(data_id)
        return data.value if data else None

    @log_method
    def clear(self):
        user_count = self.db.query(UserModel).delete()
        account_count = self.db.query(AccountModel).delete()
        self.db.commit()
        return {'user': user_count, 'account': account_count}
