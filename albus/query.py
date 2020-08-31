from typing import Sequence
from collections import namedtuple
from copy import copy

Plan = namedtuple('Plan', ['filters', 'includes', 'nested_filters',
                           'nested_includes'])


class Clause:

    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Clause):
            return False
        same_fields = (
            self.field == other.field
            and self.operator == other.operator
            and self.value == other.value
        )
        return same_fields


class Plan:

    def __init__(self,
                 columns: Sequence[str],
                 filters: Sequence[Clause],
                 includes: Sequence[Clause],
                 nested_filters: Sequence['Plan'],
                 nested_includes: Sequence['Plan']):
        self.columns = copy(columns)
        self.filters = copy(filters)
        self.includes = copy(includes)
        self.nested_filters = copy(nested_filters)
        self.nested_includes = copy(nested_includes)

    def __eq__(self, other):
        if not isinstance(other, Plan):
            return False
        same_fields = (
            self.columns == other.columns
            and self.filters == other.filters
            and self.includes == other.includes
            and self.nested_filters == other.nested_filters
            and self.nested_includes == other.nested_includes
        )
        return same_fields


class BaseQuery:

    def __init__(self):
        self._filters = []
        self._includes = []
        self._nested_filters = []
        self._nested_includes = []

    def get_plan(self):
        columns = self.get_columns()
        snapshot = Plan(
            columns,
            copy(self._filters),
            copy(self._includes),
            copy(self._nested_filters),
            copy(self._nested_includes),
        )
        return snapshot

    def get_columns(self):
        return ['*']

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

    def get_columns(self):
        columns = []
        for attr_name, field in self._model.enumerate_fields():
            columns.append(field.name)
        return columns
