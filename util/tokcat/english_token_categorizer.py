from util.english.personal import PersonalsManager
from util.english.verb import Conjugator
from util.tokcat.token_categorizer import TokenCategorizer
from util.tokcat.precompute.personal_evaluators import PersProEvaluator, PosDetEvaluator
from util.tokcat.precompute.verb_evaluator import VerbEvaluator
from util.tokcat.dynamic.number_evaluator import NumberEvaluator


class EnglishTokenCategorizer(TokenCategorizer):
    def __init__(self, expressions):
        personals_mgr = PersonalsManager.init_default()
        conjugator = Conjugator.init_default()

        key2closed = {
            'perspro': PersProEvaluator(personals_mgr),
            'posdet':  PosDetEvaluator(personals_mgr),
            'to':      VerbEvaluator(conjugator),
        }

        key2open = {
            'number': NumberEvaluator(),
        }

        super(EnglishTokenCategorizer, self).__init__(
            key2closed, key2open, expressions)
