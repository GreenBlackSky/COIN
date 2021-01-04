from nameko.rpc import rpc


class DBService:
    name = "db_service"

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)