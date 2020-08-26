class Architect:

    def __init__(self, con):
        assert con is not None, "Architect needs a connection"
        self._con = con


class Engine:

    ddl_class = None

    def __init__(self):
        self._con = None
        self._ddl = None
        self.connect()

    @property
    def ddl(self):
        if self._ddl is None:
            self._ddl = type(self).ddl_class(self._con)
        return self._ddl

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        if self._con is not None:
            self._con.close()
        self._con = None
