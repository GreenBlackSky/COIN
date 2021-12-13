"""Some common for project constants."""

# from .schemas import UserSchema, AccountSchema, \
#     CategorySchema, EventSchema, TemplateSchema


# class ENTITY:
#     """App entity type."""

#     USER = 'user'
#     ACCOUNT = 'account'
#     CATEGORY = 'category'
#     TEMPLATE = 'template'
#     EVENT = 'event'


#     ENTITY_SCHEMAS = {
#         USER: UserSchema,
#         ACCOUNT: AccountSchema,
#         TEMPLATE: CategorySchema,
#         EVENT: TemplateSchema,
#     }


class STATUS_CODE:
    """In-app status codes."""

    pass


MAIN_ACCOUNT_NAME = "Main Account"

MAX_ACCOUNTS = 100

# TODO basic categories
STARTING_CATEGORIES = [
    {
        'name': 'base',
        'color': '000000'
    }
]

STARTING_TEMPLATES = []
