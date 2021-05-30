"""Labels logic service."""

from datetime import datetime

from nameko.rpc import rpc

from common.debug_tools import log_method
from common.schemas import LabelSchema

from .model import session, LabelModel


class LabelService:
    """Class contains logic that concerns labels."""

    name = "label_service"

    @rpc
    @log_method
    def create_label(self):
        """Create new label."""
        pass

    @rpc
    @log_method
    def get_labels(self):
        """Get events."""
        pass

    @rpc
    @log_method
    def edit_label(self):
        """Edit label."""
        pass

    @rpc
    @log_method
    def delete_label(self):
        """Delete label."""
        pass

    @rpc
    @log_method
    def clear(self):
        """Clear all labels."""
        pass
