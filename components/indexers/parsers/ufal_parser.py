import pdb

class UFALParser(object):
    def __init__(self, cfg):
        self.ignore_items = []
        self.stop_words = []
        self.symbols = [',', '.', '!', '`', '~', '#', '\"', '[', ']', '(', ')', '-', '+']
        self.ignore_items.extend(self.symbols)

    def term_iter(self, path):
        '''Return a iterator over all terms in the document given in the path.'''
        pass
    def document_term_iter(self, doc_content):
        lines = doc_content.splitlines()
        for line in lines:
            line = line.strip()
            if line=='':
                continue
            tag = self._extract_xml_tag(line)
            if tag is None:
                term = self._extract_term(line)
                if term not in self.ignore_items:
                    yield term

    def _extract_term(self, line):
        return line.split('\t')[1].strip()

    def _extract_xml_tag(self, line):
        st = line.find('<')
        fn = line.find('>')
        if st<0 or fn<0:
            return None
        return line[st:fn+1]
 
