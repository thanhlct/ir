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
        'type': None
    }
}
