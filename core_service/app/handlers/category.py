"""Module, that contains events manipulation methods."""

from celery_abc import WorkerMetaBase
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from common.celery_utils import celery_app
from common.interfaces import CategoryService
from common.schemas import CategorySchema

from .account import AccountHandler

from ..model import session, CategoryModel


category_schema = CategorySchema()


# TODO refactor account and user checks
class CategoryHandler(CategoryService, metaclass=WorkerMetaBase):
    """Class contains method for handling events categories stuff."""

    def create_category(self, user_id, account_id, name, color):
        """Create new events category."""
        accounts_response = AccountHandler.check_account_user(
            account_id,
            user_id
        )
        if accounts_response['status'] != 'OK':
            return accounts_response

        category = CategoryModel(
            user_id=user_id,
            account_id=account_id,
            name=name,
            color=color
        )
        session.add(category)
        session.commit()
        return {'status': 'OK', 'category': category_schema.dump(category)}

    def get_categories(self, user_id, account_id):
        """Get all categories user has."""
        accounts_response = AccountHandler.check_account_user(
            account_id,
            user_id
        )
        if accounts_response['status'] != 'OK':
            return accounts_response

        query = session\
            .query(CategoryModel)\
            .filter(CategoryModel.user_id == user_id)\
            .filter(CategoryModel.account_id == account_id)
        return {
            'status': 'OK',
            'categories': [
                category_schema.dump(category)
                for category in query.all()
            ]
        }

    def edit_category(
        self,
        user_id,
        account_id,
        category_id,
        name,
        color
    ):
        """Request to edit events category."""
        accounts_response = AccountHandler.check_account_user(
            account_id,
            user_id
        )
        if accounts_response['status'] != 'OK':
            return accounts_response

        category = session.get(CategoryModel, category_id)
        if category is None:
            return {'status': 'no such category'}
        if category.user_id != user_id:
            return {'status': 'accessing another users events'}
        if category.account_id != account_id:
            return {'status': 'wrong account for category'}

        category.name = name
        category.color = color

        session.commit()
        return {'status': 'OK', 'category': category_schema.dump(category)}

    def delete_category(self, user_id, account_id, category_id):
        """Delete existing events category."""
        accounts_response = AccountHandler.check_account_user(
            account_id,
            user_id
        )
        if accounts_response['status'] != 'OK':
            return accounts_response

        category = session.get(CategoryModel, category_id)
        if category is None:
            return {'status': 'no such category'}
        if category.user_id != user_id:
            return {'status': 'accessing another users events'}
        if category.account_id != account_id:
            return {'status': 'wrong account for category'}

        session.delete(category)
        session.commit()
        return {'status': 'OK', 'category': category_schema.dump(category)}


CategoryHandler(celery_app)
