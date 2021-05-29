"""Event logic service."""

from datetime import datetime

from nameko.rpc import rpc

from common.debug_tools import log_method
from common.schemas import EventSchema

from .model import session, EventModel


class EventService:
    """Class contains logic that concerns events."""

    name = "event_service"

    @rpc
    @log_method
    def create_event(self, user_id, acc_id,
                     event_time, diff, total, description, confirmed):
        """Create new event."""
        pass

    @rpc
    @log_method
    def get_events(self, acc_ids,
                   start_time, end_time,
                   with_lables, not_with_lables):
        """Get events."""
        pass

    @rpc
    @log_method
    def confirm_event(self, event_id):
        """Confirm event."""
        pass

    @rpc
    @log_method
    def edit_event(self, event_id,
                   event_time, diff, total, description):
        """Edit event."""
        pass

    @rpc
    @log_method
    def delete_event(self, event_id):
        """Delete event."""
        pass

    @rpc
    @log_method
    def clear(self):
        """Clear all events."""
        pass
