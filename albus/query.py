from collections import namedtuple
from copy import copy

Clause = namedtuple('Clause', ['field', 'operator', 'value'])


class BaseQuery:

    def __init__(self):
        self._filters = []
        self._includes = []

    @property
    def plan(self):
        snapshot = dict(
            filters=copy(self._filters),
            includes=copy(self._includes),
        )
        return snapshot

    def filter(self, clause):
        self._filters.append(clause)

    def include(self, clause):
        self._includes.append(clause)


class FilterMixin:

    def __filter(self, field, operator, value):
        clause = Clause(field, operator, value)
        self.filter(clause)

    def filter_isnull(self, field, is_null=True):
        self.__filter(field, 'isnull', is_null)

    def filter_equals(self, field, value):
        self.__filter(field, 'equals', value)

    def filter_greater(self, field, value):
        self.__filter(field, 'greater', value)

    def filter_less(self, attr_name, value):
        self.__filter(attr_name, 'less', value)


class IncludeMixin:

    def __include(self, field, operator, value):
        clause = Clause(field, operator, value)
        self.include(clause)

    def include_isnull(self, field, is_null=True):
        self.__include(field, 'isnull', is_null)

    def include_equals(self, field, value):
        self.__include(field, 'equals', value)

    def include_greater(self, field, value):
        self.__include(field, 'greater', value)

    def include_less(self, field, value):
        self.__include(field, 'less', value)


class Query(BaseQuery, FilterMixin, IncludeMixin):

    pass


class CombineMixin:

    def add_alternative(self, query):
        raise NotImplementedError()

    def add_constraint(self, query):
        raise NotImplementedError()


class UserQuery(Query, CombineMixin):

    pass


class ModelQuery(UserQuery):

    def __init__(self, model):
        self._model = model
