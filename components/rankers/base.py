class QueryResult(object):
    def __init__(self, docid=None, rank=None, score=None):
        self.docid = docid
        self.rank = rank
        self.score = score

class WeightCalculator(object):
    def __init__(self, cfg):
        pass
    def compute_term_weight(self, term, tf, scheme_type):
        pass
    def compute_norm(self, vector, shceme_type):
        pass 

class ScoreCalculator(object):
    def __init__(self, query):
        pass
    def score(doc):
        pass

class Ranker(object):
    def __init__(self, id_maker, postlist):
        pass
    def get_top_relevant_docs(self, query, top_k = 1000):
        pass
