"""Translate between db model and marshmallow schema objects."""

from common.schemas import UserSchema


class DBTranslate:

    def user_model2schema(self, user, account, date):
        return {
            'id': user.id,
            'name': user.name,
            'accounts': [account.id]
        }
