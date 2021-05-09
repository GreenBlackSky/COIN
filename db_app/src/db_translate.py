"""Translate between db model and marshmallow schema objects."""

from datetime import date as DateType

from common.debug_tools import log_method

from .models import CategoryModel, TemplateModel, UserModel, AccountModel


class DBTranslate:
    """Transalte entities models into schemas and back."""

    @log_method
    def m2s_user(self, user: UserModel):
        """Tranalte user model into user schema."""
        if user is None:
            return None
        return {
            'id': user.id,
            'name': user.name,
            'password_hash': user.password_hash
        }

    @log_method
    def m2s_account(self, account: AccountModel):
        """Translate account model into account schema."""
        if account is None:
            return None
        return {
            'id': account.id,
            'name': account.name,
        }

    @log_method
    def m2s_label(self, category):
        """Translate category model into schema."""
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "color": category.color,
            "hidden": category.hidden,
        }

    @log_method
    def template_model2schema(self, template):
        pass
