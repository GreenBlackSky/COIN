"""Translate between db model and marshmallow schema objects."""

from datetime import date as DateType

from common.schemas import UserSchema, AccountSchema, DateSchema
from common.debug_tools import log_method

class DBTranslate:

    @log_method
    def user_model2schema(self, user, accounts):
        account_schemas = [
            self.account_model2Schema(account, dates, templates, categories)
            for account, dates, templates, categories in accounts
        ]
        user_schema = {
            'id': user.id,
            'name': user.name,
            'accounts': account_schemas
        }
        return user_schema

    @log_method
    def account_model2Schema(self, account, dates, templates, categories):
        return {
            'id': account.id,
            'name': account.name,
            'dates': [
                self.date_model2schema(date, events)
                for date, events in dates
            ],
            'templates': [
                self.template_model2schema(template)
                for template in templates
            ],
            'categories': [
                self.category_model2schema(category)
                for category in categories
            ]
        }

    @log_method
    def date_model2schema(self, date, events):
        return {
            'date': str(date.date),
            'balance': date.balance,
            'unconfirmed_balance': date.unconfirmed_balance,
            'events':  [
                self.event_model2schema(event)
                for event in events
            ]
        }

    @log_method
    def template_model2schema(self, template):
        pass

    @log_method
    def category_model2schema(self, category):
        pass
