class FrequencyPostList(PostingListMaker):
    def __init__(self, cfg):
        '''Count, init everythings for later processes.'''
        pass
    #methods from general PostingListMaker
    def build_posting_list(self, doc_id_maker, parser):
        pass
    def get_posting_list(term):
        '''Return the posting list for the given term.'''
    #Methods for frequency posting list
    def get_tf(term, doc_id):
        '''Return term frequency of the given term in the given document.'''
        pass
    def get_df(term):
        '''Return document frequency of the given term.'''
        pass

class TieredFrequencyPostList(PostingListMaker):
    def __init__(self, cfg):
        pass

class TermWeighting(object):
    @classmethod
    def get_weighted_tf(tf, weighting_scheme):
        '''Get the term frequency weight for the given term and given scheme.'''
        pass
    @classmethod
    def get_weighted_df(df, weighting_scheme):
        '''Get the document frequency weight for the given term and given scheme.'''
        pass
