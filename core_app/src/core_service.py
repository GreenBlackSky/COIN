"""Core logic service."""

from hashlib import md5

from nameko.rpc import rpc, RpcProxy

from common.schemas import UserSchema
from common.debug_tools import log_method


class CoreService:
    """Class contains core logic of app."""

    name = "core_service"
    db_service = RpcProxy('db_service')

    @rpc
    @log_method
    def create_user(self, name, password):
        """Create new user."""
        password_hash = md5(password.encode()).hexdigest()
        user = self.db_service.create_user(name, password_hash)
        if user is None:
            return {'status': 'user exists'}

        return {
            'status': 'OK',
            'user': user
        }

    @rpc
    @log_method
    def get_user(self, name, password):
        """Get user by name and password."""
        user = self.db_service.get_user(name=name)
        if user is None:
            return {'status': 'no such user'}
        if user["password_hash"] != md5(password.encode()).hexdigest():
            return {'status': 'wrong password'}
        return {
            'status': 'OK',
            'user': user
        }

    @rpc
    @log_method
    def edit_user(self, user, name, old_pass, new_pass):
        """Edit user name or change password."""
        user = UserSchema().load(user)
        got_old_pass = (old_pass is not None)
        got_new_pass = (new_pass is not None)
        if got_new_pass != got_old_pass:
            return {
                'status':
                "new password must be provided with an old password"
            }

        if got_old_pass and got_new_pass:
            old_hash = md5(old_pass.encode()).hexdigest()
            if old_hash != user.password_hash:
                return {'status': 'wrong password'}
            new_hash = md5(new_pass.encode()).hexdigest()
        else:
            new_hash = None

        if name != user.name:
            other_user = self.db_service.get_user(name=name)
            if other_user:
                return {'status': 'user exists'}

        return {
            'status': 'OK',
            'user': self.db_service.edit_user(user.id, name, new_hash)
        }
