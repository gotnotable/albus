class BaseQuery:

    pass


class FilterableQuery(BaseQuery):

    def __init__(self, model):
        self._model = model

    def filter_isnull(self, attr_name, is_null=True):
        raise NotImplementedError()

    def filter_equals(self, attr_name, value):
        raise NotImplementedError()

    def filter_greater(self, attr_name, value):
        raise NotImplementedError()

    def filter_less(self, attr_name, value):
        raise NotImplementedError()


class CombinableQuery(FilterableQuery):

    def add_alternative(self, query):
        raise NotImplementedError()

    def add_constraint(self, query):
        raise NotImplementedError()
