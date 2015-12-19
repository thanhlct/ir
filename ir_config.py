from ir.utils.config import as_project_path
from ir.indexers.docid_makers.count_id_maker import CountIDMaker
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
    'parser':{
        'type': None,
        'debug': True,
        'SimpleParser':{
            'temporary_file': as_project_path('private/temporary_files/parser_results.pkl'),
        },
        'MultiProcessParser':{
            'temporary_file': as_project_path('private/temporary_files/parser_results.pkl'),
            'block_size': 1000,
            'sleep_for_result': 10,
            'max_thread_used':2,#not supported since RAM too big
        },
    }
}
