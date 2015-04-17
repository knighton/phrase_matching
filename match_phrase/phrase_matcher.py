from categorize_token.expression import Expression
from categorize_token.token_categorizer import TokenCategorizer
from match_phrase.block_parser import BlockParser
from match_sequence.list_sequence_matcher import ListSequenceMatcher


class PhraseMatcher(object):
    """
    Matches phrases.

    Initialized with all the expressions that it will recognize.  Then when it
    receives tokens, converts them to lists of (category IDs + the token) before
    sending them to the ListSequenceMatcher for analysis.
    """

    def __init__(self, key2closed_class_evaluator, key2open_class_evaluator,
                 blocks_as_expr_lines):
        # Process the input config lines into a format we can use, extracting
        # the Expressions that we will recognize instances of.
        parser = BlockParser()
        blocks_as_exprs = parser.parse_blocks(blocks_as_expr_lines)
        expressions = self._expressions_from_blocks_as_exprs(blocks_as_exprs)
        self._token_categorizer = TokenCategorizer(
            key2closed_class_evaluator, key2open_class_evaluator, expressions)
        blocks_as_lists = self._make_blocks_as_lists(blocks_as_exprs)

        # Create the sequence matcher.
        self._list_sequence_matcher = ListSequenceMatcher(blocks_as_lists)

    def _expressions_from_blocks_as_exprs(self, blocks_as_exprs):
        """
        blocks as exprs -> list of all Expression present
        """
        rr = []
        for block in blocks_as_exprs:
            for option in block:
                for a in option:
                    if isinstance(a, Expression):
                        rr.append(a)
        return rr

    def _make_blocks_as_lists(self, blocks_as_exprs):
        for block in blocks_as_exprs:
            for option in block:
                for a in option:
                    if isinstance(a, basestring):
                        new_option.append(a)
                    elif isinstance(a, Expression):
                        cat_id = self._token_categorizer.get_category_id(a)
                        new_option.append(cat_id)
                    else:
                        assert False

    def _preprocess_input_tokens(self, ss):
        """
        list of token -> list of list of 'value'

        Used to make input in the right format for the ListSequenceMatcher.
        """
        rr = []
        for s in ss:
            cat_ids = self._token_categorizer.get_category_ids_for_token(s)
            rr.append([s] + cat_ids)
        return rr

    def each_match_list(self, ss):
        items = self._preprocess_input_tokens(ss)
        for match_list in self._list_sequence_matcher.each_match_list(items):
            yield match_list
