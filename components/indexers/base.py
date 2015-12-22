class DocIDMaker(object):
    def __init__(self, cfg):
        pass
    def make_id_for_directories(self, *paths):
        '''Given ids for all document directories given in paths (list of path).'''
        pass
    def make_id_from_file(self, document_list_file):
        '''Given ids for all documents listed int he document_list_file.'''
        pass
    def __getitem__(self, doc_id):
        """Get information about doc_id, path, and so on."""
        pass
    def __len__(self):
        '''Return the number of document that the DocIder manage.'''
        pass
    def __iter__(self):
        """Return Iterator over all document."""
        pass
    def get_sub_id_maker(self, from_index, to_index):
        """Get a DocIDMaker which comprises all document with the range of indexes given."""
        pass

class Parser(object):
    def __init__(self, cfg):
        pass
    def term_iter(self, path):
        '''Return a iterator over all terms in the document given in the path.'''
        pass
    def document_term_iter(self, doc_content):
        pass

class PostingListMaker(object):
    def __init__(self, cfg):
        pass
    def build_from_id_maker(self, id_maker, parser):
        '''Buid posting list for all docuent in the docid_maker given.'''
        #TODO: parser should be taken from configuration
        pass
    def build_from_documents(self, docs, parser):
        '''Buid posting list for all documents given.'''
       pass 
    def get_posting_list(term):
        '''Get a full posting list of the term given.'''
        pass
    def get_doc_vector(doc_id):
        '''Get a vector presetnation of a document specified by doc_id.'''
        pass

class TierSeparator(object):
    def __init__(self, cfg):
        pass
    def separate_tiers_from_path(self, path):
        '''Return a list of tiered content from the given document.'''
        pass
    def separate_tiers_from_doc(self, doc_content):
        '''Return a list of tiered content from the given document.'''
        pass

class TieredPostingListMaker(object):
    def __init__(self, cfg):
        pass
    def build_from_id_maker(self, id_maker, tier_separator, parser):
        pass
    
class Indexer(object):
    '''Return the vector representation of the given document/query.
    
    We calculate for only term occured in query so that class probabily doesn't nessary
    '''
    pass
