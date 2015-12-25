import os

from ir.utils.support_functions import deep_copy
from ir.utils.io_functions import file_exists, file_to_object, object_to_file

class CountIDMaker(object):
    def __init__(self, cfg):
        self.id_mapping = {}
        self.name = self.__class__.__name__
        self.full_config = cfg
        self.config = cfg['docid_maker'][self.name]

    def make_id_for_paths(self, *paths):
        raise NotImplementedError('You didnt implemented this method!, make id for all document in the list of dicrectoies given')
   
    def _read_mapping(self):
        path = self.config['docid_mapping_file']
        if file_exists(path):
            print 'Read docid_mapping from [%s]'%path
            return file_to_object(path)
        else:
            return None

    def _write_mapping(self, id_mapping):
        path = self.config['docid_mapping_file']
        print 'Saving docid_mapping result to [%s]'%path
        object_to_file(id_mapping, path) 

    def make_id_from_file(self, document_list_file=None, add_data_path=True):
        saved_id_mapping = self._read_mapping()
        if saved_id_mapping is not None:
            self.id_mapping = saved_id_mapping
            self.id_keys = self.id_mapping.keys()
            return

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
        #self.total_doc_number=count
        self.id_keys = self.id_mapping.keys()
        self._write_mapping(self.id_mapping)

    def __getitem__(self, doc_id):
        return self.id_mapping[doc_id]

    def __len__(self):
        return len(self.id_mapping) #self.total_doc_number
    def __iter__(self):
        for doc_id in self.id_mapping.keys():
            yield doc_id, self[doc_id]

    def get_sub_id_maker(self, from_id, to_id):
        maker = CountIDMaker(self.full_config)
        for key in self.id_keys[from_id: to_id]:
            maker.id_mapping[key] = deep_copy(self[key])
        return maker
