from ir.utils.config import as_project_path
from ir.components.indexers.docid_makers.count_id_maker import CountIDMaker
from ir.utils.support_functions import read_gz_text_file
#from ir.indexers.parsers.

config={
    'general':{
        'data_path': as_project_path('private/data/A1/'),
    },
    'indexer':{
        'type': None,
        'debug': True,
    },
    'docid_maker':{
        'type': CountIDMaker,
        'debug': True,
        'CountIDMaker':{
            'document_list_file': as_project_path('private/data/A1/documents.list'),
        },
    },
    'postlist_maker':{
        'type': None,
        'debug': True,
        'FrequencyPostList':{
            'read_file_fun': read_gz_text_file,
            'postlist_file': as_project_path('private/temporary_files/postlist_results.pkl'),
            'block_size': 10,
            'sleep_for_result': 2,
            'limited_process_number':3,
        },
    },
}
