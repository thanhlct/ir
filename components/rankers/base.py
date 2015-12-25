class QueryResult(object):
    def __init__(self, docid=None, score=None, rank=None):
        self.docid = docid
        self.rank = 0
        self.score = score

    def __str__(self):
        return '%d\t%d\t%f'%(self.docid, self.rank, self.score)

    def __lt__(self, o):
        return self.score < o.score
    
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
