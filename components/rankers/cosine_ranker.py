import pdb

from ir.components.rankers.base import Ranker, QueryResult

class CosineRanker(Ranker):
    def __init__(self, id_maker, postlist, weight_calculator):
        self.id_maker = id_maker
        self.postlist = postlist
        self.weight_calculator = weight_calculator

    def get_top_relevant_docs(self, query, top_k = 1000):
        scores = {}
        query_vector = []
        doc_vectors = {}
        for term in query:
            if term not in self.postlist.keys():#ignore term not existed in train documetn
                continue
            w_tq = self.weight_calculator.compute_term_weight(term, 1, scheme_type='query')
            query_vector.append(w_tq)
            t_postlist = self.postlist[term]
            for doc_id in t_postlist.keys():
                tf = t_postlist[doc_id]
                w_td = self.weight_calculator.compute_term_weight(term, tf, scheme_type='doc')
                if doc_id not in scores.keys():
                    scores[doc_id] = 0
                    doc_vectors[doc_id] = []
                scores[doc_id] += w_tq*w_td
                doc_vectors[doc_id].append(w_td)
        
        #normalisation
        results = []
        query_norm = self.weight_calculator.compute_norm(query_vector, scheme_type='query')
        for doc_id in scores.keys():
            doc_norm = self.weight_calculator.compute_norm(doc_vectors[doc_id], scheme_type='doc')
            scores[doc_id] /= query_norm*doc_norm
            results.append(QueryResult(doc_id, scores[doc_id]))

        results.sort()
        results.reverse()
        return results[0:top_k]
