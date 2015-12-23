import autopath
import pdb

from multiprocessing import Process, Queue, Pipe

from ir.components.indexers.base import PostingListMaker
from ir.utils.timecount import TimeStats

class FrequencyPostList(PostingListMaker):
    def __init__(self, cfg):
        '''Count, init everythings for later processes.'''
        self.full_config = cfg
        self.name = self.__class__.__name__
        self.config = cfg['postlist_maker'][self.name]
        self.block_size = self.config['block_size']
        self.sleep_for_result = self.config['sleep_for_result']
        self.read_file_fun = self.config['read_file_fun']

        self.timer = TimeStats()
    #----------------------methods from general PostingListMaker
    def build_from_id_maker(self, id_maker, parser):
        self.timer.start_clock('read_file')
        docs = []
        for doc_id, doc_des in id_maker:
            content = self.read_file_fun(doc_des['path']) 
            docs.append({'doc_id': doc_id, 'content': content,})
        self.timer.end_clock('read_file')
        print 'Read all %d files in %s'%(len(id_maker), self.timer.show_time('read_file', level='hour'))
        self.build_from_documents(docs, parser)

    def build_from_documents(self, docs, parser):
        #Contiunue here, buid postlist for each block and then code the block process and merge process        
        pass
    def get_posting_list(term):
        '''Return the posting list for the given term.'''
        raise NotImplementedError('FrequencyPostList.get_posting_list was not implemented.')
    #-------------------Methods for frequency posting list

    def get_tf(term, doc_id):
        '''Return term frequency of the given term in the given document.'''
        pass
    def get_df(term):
        '''Return document frequency of the given term.'''
        pass

class PostListMergeProcess(Process):
    def __init__(self, result_queue):
        self.result = result_queue
        self.postlist = {}

    def run(self):
        while True:
            
        

class PostListBuildProcess(Process):
    def __init__(self, docs, parser, result_queue):
        self.docs = docs
        self.parser = parser
        self.result = result_queue

    def run(self):
        pass
        

#------------Testing----------------
from ir.utils.config import Config
from ir.components.indexers.docid_makers.count_id_maker import CountIDMaker
from ir.components.indexers.parsers.ufal_parser import UFALParser


def main():
    config = Config.load_configs(['../../../ir_config.py'], use_default=False, log=False)
    id_maker = CountIDMaker(config)
    id_maker.make_id_from_file()
    id_maker = id_maker.get_sub_id_maker(0, 99)
    postlist_maker = FrequencyPostList(config)
    parser = UFALParser(config)
    postlist = postlist_maker.build_from_id_maker(id_maker, parser)  

if __name__=='__main__':
    main()

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
