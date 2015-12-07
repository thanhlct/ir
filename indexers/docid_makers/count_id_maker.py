import os

class CountIDMaker(object):
    def __init__(self, cfg):
        self.id_mapping = {}
        self.name = self.__class__.__name__
        self.full_config = cfg
        self.config = cfg['docid_maker'][self.name]

    def make_id_for_paths(self, *paths):
        raise NotImplementedError('You didnt implemented this method!, make id for all document in the list of dicrectoies given')

    def make_id_from_file(self, document_list_file=None, add_data_path=True):
        if document_list_file is None:
            document_list_file = self.config['document_list_file']
        with open(document_list_file, 'r') as f:
            count = 0
            for line in f.readlines():
                line = line.strip()
                count +=1
                data_path = ''
                if add_data_path:
                    data_path = self.full_config['general']['data_path']
                path = os.path.join(data_path, line + '.gz')
                _, filename = os.path.split(path)
                filename = filename.split('.')[0]
                self.id_mapping[count-1]={'path': path, 'filename': filename}
        self.total_doc_number=count

    def __getitem__(self, doc_id):
        return self.id_mapping[doc_id]

    def __len__(self):
        return self.total_doc_number
    def __iter__(self):
        for doc_id in self.id_mapping.keys():
            yield doc_id, self[doc_id]
