"""Translate between db model and marshmallow schema objects."""

from datetime import date as DateType

from common.schemas import UserSchema, AccountSchema
from common.debug_tools import log_method


class DBTranslate:

    @log_method
    def user_model2schema(self, user, accounts):
        user_schema = {
            'id': user.id,
            'email': user.email,
            'accounts': [acc.id for acc in accounts]
        }
        return user_schema

    @log_method
    def account_model2Schema(self, account, templates, categories):
        return {
            'id': account.id,
            'name': account.name,
            'actual_date': None,
            'balance': None,
            'unconfirmed_balance': None,
            'templates': [template.id for template in templates],
            'categories': [category.id for category in categories]
        }

    @log_method
    def template_model2schema(self, template):
        pass

    @log_method
    def category_model2schema(self, category):
        pass
