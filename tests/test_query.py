from unittest import TestCase

from albus.field import IntegerField, StringField
from albus.query import Clause, Query


class BaseQueryTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query = None

    @property
    def query(self) -> Query:
        if self._query is None:
            self._query = Query()
            self.addCleanup(self.cleanupQuery)
        return self._query

    def cleanupQuery(self):
        if self._query is not None:
            self._query = None

    def assertPlanEqual(self, expected):
        got = self.query.get_plan()
        self.assertEqual(expected, got)


class SimpleQueryTest(BaseQueryTest):

    def setUp(self):
        self.title_field = StringField()
        self.rank_field = IntegerField()

    def test_filter_equals(self):
        self.query.filter_equals(self.title_field, 'Some Book')
        expected_plan = dict(
            filters=dict(
                clauses=[Clause(self.title_field, 'equals', 'Some Book')],
                nested=[],
            ),
            includes=dict(
                clauses=[],
                nested=[],
            ),
        )
        self.assertPlanEqual(expected_plan)

    def test_filter_with_include(self):
        self.query.filter_equals(self.title_field, 'Top Book')
        self.query.include_less(self.rank_field, 10)
        expected_plan = dict(
            filters=dict(
                clauses=[Clause(self.title_field, 'equals', 'Top Book')],
                nested=[],
            ),
            includes=dict(
                clauses=[Clause(self.rank_field, 'less', 10)],
                nested=[],
            ),
        )
        self.assertPlanEqual(expected_plan)


class NestedQueryTest(BaseQueryTest):

    def setUp(self):
        self.maxDiff = None
        self.title_field = StringField()
        self.rank_field = IntegerField()

    def test_verbose_range(self):
        # (title > A or title = A) and title < B
        nested = Query()
        nested.include_greater(self.title_field, 'A')
        nested.include_equals(self.title_field, 'A')
        self.query.filter_query(nested)
        self.query.filter_less(self.title_field, 'B')
        nested_plan = dict(
            filters=dict(
                clauses=[],
                nested=[],
            ),
            includes=dict(
                clauses=[
                    Clause(self.title_field, 'greater', 'A'),
                    Clause(self.title_field, 'equals', 'A')],
                nested=[],
            ),
        )
        expected_plan = dict(
            filters=dict(
                clauses=[Clause(self.title_field, 'less', 'B')],
                nested=[nested_plan],
            ),
            includes=dict(
                clauses=[],
                nested=[],
            ),
        )
        self.assertPlanEqual(expected_plan)
