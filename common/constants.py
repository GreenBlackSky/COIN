"""Some common for project constants."""

from .schemas import UserSchema, AccountSchema, \
    CategorySchema, EventSchema, TemplateSchema


class ENTITY:
    """App entity type."""

    USER = 'user'
    ACCOUNT = 'account'
    CATEGORY = 'category'
    TEMPLATE = 'template'
    EVENT = 'event'


ENTITY_SCHEMAS = {
    ENTITY.USER: UserSchema,
    ENTITY.ACCOUNT: AccountSchema,
    ENTITY.TEMPLATE: CategorySchema,
    ENTITY.EVENT: TemplateSchema,
}

MAIN_ACCOUNT_NAME = "Account"
