import pdb
from multiprocessing import Process, Queue
import time

from ir.utils.support_functions import read_gz_text_file, read_gz_file, gz_text_file_line_iter
from ir.utils.timecount import TimeStats
from ir.utils.io_functions import object_to_file, file_to_object

class OneBlockParser(Process):
    def __init__(self, name, id_maker, result_queue):
        Process.__init__(self)
        self.name = name
        self.id_maker = id_maker
        self.result_queue = result_queue
        
        self.time_stat = TimeStats()

        self.title_posting_list = {}
        self.heading_posting_list = {}
        self.geography_posting_list = {}
        self.text_posting_list = {}
        self.posting_lists = [self.title_posting_list, self.heading_posting_list, self.geography_posting_list, self.text_posting_list]

    def run(self):
        self.time_stat.start_clock('block')

        self.parse_one_id_maker(self.id_maker)
        self.result_queue.put((self.name, self.posting_lists), block=False)

        self.time_stat.end_clock('block')
        print '---%s (%d docs) finisned after %s'%(self.name, len(self.id_maker), self.time_stat.show_time('block', level='minute'))

    def parse_one_id_maker(self, id_maker):
        count = 0
        for doc_id, doc_des in id_maker:
            #print '%s: %d: %s'%(self.name, doc_id, doc_des['path'])
            self.parse_a_document(doc_id, doc_des['path'])
            count +=1
            if count%50==0:
                print '%s processed %d/%d after %s'%(self.name, count, len(id_maker), self.time_stat.show_time('block', level='hour'))

    def parse_a_document(self, doc_id, path):
        posting_list = None
        for line in gz_text_file_line_iter(path):
            line = line.strip()
            if line=='':
                continue
            tag = self._extract_xml_tag(line)
            if tag is not None:#new part of the document
                posting_list = self.get_posting_list(tag)
                continue
            if posting_list == None:#no posting list was activited, ignore the word
                print '******Warning: the line [%s] was ignored'%line
                continue
            term = self._extract_term(line)
            if term in posting_list.keys():
                posting_list[term].add(doc_id)
            else:
                posting_list[term] = set([doc_id])

    def _extract_term(self, line):
        #print '---', line
        return line.split('\t')[1]

    def _extract_xml_tag(self, line):
        st = line.find('<')
        fn = line.find('>')
        if st<0:
            return None
        return line[st:fn+1]
 
    def get_posting_list(self, xml_tag):
        if xml_tag == '<TITLE>':
            #print '---active TITLE'
            return self.title_posting_list
        elif xml_tag == '<GEOGRAPHY>':
            #print '---active GEO'
            return self.geography_posting_list
        elif xml_tag == '<HEADING>':
            #print '---active HEADING'
            return self.heading_posting_list
        elif xml_tag == '<TEXT>':
            #print '---active TEXT'
            return self.text_posting_list
        else:
            return None

class MultiProcessParser(object):
    def __init__(self, config):
        self.full_config = config
        self.name = self.__class__.__name__
        self.config = config['parser'][self.name]
        self.block_size = self.config['block_size']
        self.sleep_for_result = self.config['sleep_for_result']

        self.title_posting_list = {}
        self.heading_posting_list = {}
        self.geography_posting_list = {}
        self.text_posting_list = {}
        self.posting_lists = [self.title_posting_list, self.heading_posting_list, self.geography_posting_list, self.text_posting_list]

        self.time_stat = TimeStats()


    def parse_an_id_maker(self, id_maker):
        self.time_stat.start_clock('parser')
        pros = []
        result_q = Queue()
        split = 0
        thread_count = 0
        while split<len(id_maker):
            thread_count +=1
            sub_id_maker = id_maker.get_sub_id_maker(split, split+self.block_size-1)
            name = 'Thread %d'%thread_count
            p = OneBlockParser(name, sub_id_maker, result_q)
            pros.append(p)
            p.start()
            #p.join()
            split += self.block_size

            if thread_count == 3:
                break
        print '---Started total %d parsing threads'%thread_count
        
        result_count = 0
        while(result_count<thread_count):
            if result_q.empty():
                print 'wait for %d seconds for new results'%self.sleep_for_result
                time.sleep(self.sleep_for_result)
            else:
                thread_name, result_list = result_q.get(block=False)
                result_count +=1
                print '---Get result of %s (%d/%d) after %s'%(thread_name, result_count, thread_count, self.time_stat.show_time('parser', level='day'))

                self.time_stat.start_clock('merge')
                self.merge_into_posting_lists(result_list)
                self.time_stat.end_clock('merge')
                print '\t'*10,'(merge %s in %s)'%(thread_name, self.time_stat.show_time('merge', level='minute'))
                self.time_stat.reset_clock('merge')

        self.time_stat.end_clock('parser')
        print '---Parsing all document tooks', self.time_stat.show_time('parser')
        object_to_file(self.posting_lists, self.config['temporary_file']) 
                
    def merge_into_posting_lists(self, result_list):
        for i in range(len(result_list)):
            for key in result_list[i].keys():
                if key in self.posting_lists[i].keys():
                    self.posting_lists[i][key] = self.posting_lists[i][key].union(result_list[i][key])
                else:
                    self.posting_lists[i][key] = result_list[i][key]
