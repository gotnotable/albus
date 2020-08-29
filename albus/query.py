from collections import namedtuple
from copy import copy

Clause = namedtuple('Clause', ['field', 'operator', 'value'])
Plan = namedtuple('Plan', ['filters', 'includes', 'nested_filters',
                           'nested_includes'])


class BaseQuery:

    def __init__(self):
        self._filters = []
        self._includes = []
        self._nested_filters = []
        self._nested_includes = []

    def get_plan(self):
        snapshot = Plan(
            copy(self._filters),
            copy(self._includes),
            copy(self._nested_filters),
            copy(self._nested_includes),
        )
        return snapshot

    def filter(self, clause):
        self._filters.append(clause)

    def include(self, clause):
        self._includes.append(clause)

    def filter_query(self, query):
        sub_plan = query.get_plan()
        self._nested_filters.append(sub_plan)

    def include_query(self, query):
        sub_plan = query.get_plan()
        self._nested_includes.append(sub_plan)


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


class ModelQuery(Query):

    def __init__(self, model):
        super().__init__()
        self._model = model
