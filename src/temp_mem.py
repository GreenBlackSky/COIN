"""Temporary data storage."""
# TODO setup postgresql db
# TODO use three separate lists


class Storage:
    """Singleton data storage. Don't actualy use."""

    instance = None

    @staticmethod
    def get_instance():
        """Access method."""
        if Storage.instance is None:
            Storage.instance = Storage()
        return Storage.instance

    def __init__(self):
        """Initialize storage."""
        self.users = set()
        self.checkpoint = {}
        self.events = {}
