import autopath
import pdb

from multiprocessing import Process, Queue, Pipe, Event
import time

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
        self.process_number = self.config['limited_process_number']

        self.timer = TimeStats()
    #----------------------methods from general PostingListMaker
    def build_from_id_maker(self, id_maker, parser):
        self.timer.start_clock('read_file')
        docs = []
        for doc_id, doc_des in id_maker:
            content = self.read_file_fun(doc_des['path']) 
            docs.append({'doc_id': doc_id, 'content': content,})
            #pdb.set_trace()
        self.timer.end_clock('read_file')
        print 'Read all %d files in %s'%(len(id_maker), self.timer.show_time('read_file', level='minute'))
        self.build_from_documents(docs, parser)

    def build_from_documents(self, docs, parser):
        #Contiunue here, buid postlist for each block and then code the block process and merge process
        self.close_event = Event()
        pros = []
        result_queue = Queue()
        self.count_parent, count_child = Pipe() 
        merge_pro = PostListMergeProcess(result_queue, self.close_event, count_child, self.sleep_for_result)
        merge_pro.name = 'MergeResult'
        pros.append(merge_pro)
        merge_pro.start()

        split = 0
        self.thread_count = 0
        self.result_count = 0
        while split<len(docs):
            self.thread_count +=1
            name = 'Thread %d'%self.thread_count
            p = PostListBuildProcess(name, docs, parser, result_queue, split, min(split + self.block_size, len(docs)))
            pros.append(p)
            p.start()
            split += self.block_size
            self._loop_for_free_process() 

        while self.result_count<self.thread_count:
            time.sleep(self.sleep_for_result)
            self._update_result_received_count()

        self.close_event.set()

    def _loop_for_free_process(self):
        while self.thread_count-self.result_count>=self.process_number:
            print 'wait for free processs'
            time.sleep(self.sleep_for_result)
            self._update_result_received_count()

    def _update_result_received_count(self):
        while self.count_parent.poll():
            c = self.count_parent.recv()
            self.result_count += c
            

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
    def __init__(self, result_queue, close_event, count_child, sleep_for_result):
        Process.__init__(self)
        self.queue = result_queue
        self.postlist = {}
        self.close_event = close_event
        self.count_child = count_child
        self.sleep_for_result = sleep_for_result

    def run(self):
        while True:
            if self.close_event.is_set():
                break

            if self.queue.empty():
                print '%s sleep for %ds'%(self.name, self.sleep_for_result)
                time.sleep(self.sleep_for_result)
            else:
               thread_name, postlist = self.queue.get(block=False)
               #Continue here: merging the result....
               self.count_child.send(1)
               print '%s finished'%thread_name


class PostListBuildProcess(Process):
    def __init__(self, name, docs, parser, result_queue, from_index=None, to_index=None, postlist=None):
        '''Process from from_index to to_index -1.'''
        Process.__init__(self)
        self.name = name
        self.docs = docs
        self.queue = result_queue
        self.parser = parser
        self.from_index = from_index if from_index is not None else 0
        self.to_index = to_index if to_index is not None else len(docs)
        self.postlist = postlist if postlist is not None else {}

    def run(self):
        for i in range(self.from_index, self.to_index):
            doc_id = self.docs[i]['doc_id']
            content = self.docs[i]['content']
            print '--------process docid=', doc_id
            self.add_content(doc_id, content)
            #pdb.set_trace()
        self.queue.put((self.name, self.postlist), block=False)
            
    def add_content(self, doc_id, content):
        for term in self.parser.document_term_iter(content):
            #print term
            if term not in self.postlist.keys():
                self.postlist[term] = {doc_id: 1}
            else:
                if doc_id in self.postlist[term].keys():
                    self.postlist[term][doc_id] += 1
                else:
                    self.postlist[term][doc_id] = 1
                    
            
        

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
