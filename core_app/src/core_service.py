"""Core logic service."""

from nameko.rpc import rpc

from common.debug_tools import log_method


class CoreService:
    """
    Class contains core logic of app.

    It serves as proxy between api and db.
    """

    name = "core_service"

    @rpc
    @log_method
    def connection_test(self):
        """Test connection."""
        return 'ok'
