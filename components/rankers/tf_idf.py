import math

from ir.components.rankers.base import WeightCalculator

class TFIDFWeightCalculator(WeightCalculator):
    def __init__(self, cfg, postlist):
        self.full_config = cfg
        self.name = self.__class__.__name__
        self.config = cfg['weight_calculator'][self.name]
        self.postlist = postlist
        self.query_scheme = self.config['query_scheme']
        self.doc_scheme = self.config['doc_scheme'] 

    def compute_term_weight(self, term, tf, scheme_type):
        scheme = self.doc_scheme if scheme_type=='doc' else self.query_scheme
        tf = self._compute_tf_scheme(scheme[0],tf)
        df = len(self.postlist[term])
        idf = self._compute_idf_scheme(scheme[1], df)
        return tf*idf

    def _compute_tf_scheme(self, scheme, tf):
        if scheme=='n':
            return tf
        elif scheme=='l':
            return 1 + math.log10(tf)
        elif scheme=='a':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        elif scheme=='b':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        elif scheme=='L':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        else:
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)

    def _compute_idf_scheme(self, scheme, df):
        if scheme=='n':
            return 1
        elif scheme=='t':
            return math.log10(float(self.N)/df)
        elif scheme=='p':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        else:
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)

    def compute_norm(self, vector, scheme_type):
        scheme = self.doc_scheme if scheme_type=='doc' else self.query_scheme
        scheme = scheme[2]
        if scheme=='n':
            return 1
        elif scheme=='c':
            return math.sqrt(sum([w*w for w in vector]))
        elif scheme=='u':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        elif scheme=='b':
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
        else:
            raise NotImplementedError('tf_scheme=%s was not implemented'%scheme)
 

            

        
        
