import pdb

from ir.utils.support_functions import read_gz_text_file, read_gz_file, gz_text_file_line_iter
from ir.utils.timecount import TimeStats
from ir.utils.io_functions import object_to_file, file_to_object

class SimpleParser(object):
    def __init__(self, config):
        self.full_config = config
        self.name = self.__class__.__name__
        self.config = config['parser'][self.name]

        self.title_posting_list = {}
        self.heading_posting_list = {}
        self.geography_posting_list = {}
        self.text_posting_list = {}
        self.posting_lists = [self.title_posting_list, self.heading_posting_list, self.geography_posting_list, self.text_posting_list]

        self.time_stat = TimeStats()

    def parse_an_id_maker(self, id_maker):
        self.time_stat.start_clock('parser')
        processed = 0
        for doc_id, doc_des in id_maker:
            #print '--------process doc_id', doc_id, '|', doc_des['filename']
            self.parse_a_document(doc_id, doc_des['path'])
            processed +=1
            if processed%10==0:
                print '......%d/%d took %s'%(processed, len(id_maker), self.time_stat.show_time('parser'))
                break
                #pdb.set_trace()

        self.time_stat.end_clock('parser')
        print 'Parsing all document tooks', self.time_stat.show_time('parser')
        object_to_file(self.posting_lists, self.config['temporary_file'])
        pdb.set_trace()

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

    def _extract_term(self, line):
        #print '---', line
        return line.split('\t')[1]
        
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
                continue
            term = self._extract_term(line)
            if term in posting_list.keys():
                posting_list[term].add(doc_id)
            else:
                posting_list[term] = set([doc_id])
    
    def _extract_xml_tag(self, line):
        st = line.find('<')
        fn = line.find('>')
        if st<0:
            return None
        return line[st:fn+1]
