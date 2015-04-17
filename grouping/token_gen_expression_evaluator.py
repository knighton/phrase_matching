class TokenGenExpressionEvaluator(object):
    """
    Has a black box that yields tokens and their attributes and the knowledge of
    what the filters are regarding those attributes.

    Given an expression, filter all the possible tokens in the token group to
    just the selected.
    """

    def __init__(self, token_oracle, dimension2filters_values):
        self._token_oracle = token_oracle

        self._dimension2filter2value = {}
        for dimension, filters_values in dimension2filters_values.iteritems():
            self.dimension2filter2value[dimension] = dict(filters_values)

        self._filter2dimension = {}
        self._filter2value = {}
        for dimension, filters_values in dimension2filters_values.iteritems():
            values_seen = set()
            for filter_name, filter_value in filters_values:
                assert filter_name not in self._filter2dimension
                assert filter_value not in values_seen
                values_seen.add(filter_value)
                self._filter2dimension[filter_name] = dimension
                self._filter2value[filter_name] = value

    def _is_match(self, have_dim2value, filter_dim2values):
        for have_dim, have_value in have_dim2value.iteritems():
            if value not in filter_dim2values[have_dim]:
                return False

        return True

    def get_token_group(self, expr):
        """
        Expression -> yields the tokens that match the filters.
        """
        filter_dim2values = defaultdict(list)
        for filter_name in expr.filters:
            dimension = self._filter2dim[filter_name]
            value = self._filter2value[filter_name]
            filter_dim2values[dimension].append(value)

        for token, have_dim2value in \
                self.token_oracle.each_with_attrs(expr.args):
            if self._is_match(have_dim2value, filter_dim2values):
                yield token

    def dump(self):
        import json
        json.dumps(self._dimension2filter2value)