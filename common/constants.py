"""Some common for project constants."""

from .schemas import UserSchema, AccountSchema, DateSchema, \
    CategorySchema, EventSchema, TemplateSchema


class ENTITY:
    """App entity type."""

    USER = 'user'
    ACCOUNT = 'account'
    CATEGORY = 'category'
    TEMPLATE = 'template'
    DATE = 'date'
    EVENT = 'event'


ENTITY_SCHEMAS = {
    ENTITY.USER: UserSchema,
    ENTITY.ACCOUNT: AccountSchema,
    ENTITY.CATEGORY: DateSchema,
    ENTITY.TEMPLATE: CategorySchema,
    ENTITY.DATE: EventSchema,
    ENTITY.EVENT: TemplateSchema,
}

MAIN_ACCOUNT_NAME = "Account"
