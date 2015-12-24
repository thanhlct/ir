import pdb
import os
import argparse

import autopath
from ir.utils.config import Config
from ir.components.indexers.docid_makers.count_id_maker import CountIDMaker
from ir.components.indexers.parsers.ufal_parser import UFALParser
from ir.components.indexers.postlist_builder.frequency_postlist import FrequencyPostList

config = None

def do_queries():
    pass

def main():
    id_maker = CountIDMaker(config)
    id_maker.make_id_from_file()
    id_maker = id_maker.get_sub_id_maker(0, 99)

    postlist_maker = FrequencyPostList(config)
    parser = UFALParser(config)
    postlist = postlist_maker.build_from_id_maker(id_maker, parser)

    #pdb.set_trace()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Runing first exercise of NPFL103')
    parser.add_argument('-q', metavar='query.list', dest='query', help='A file with a list of topic filenames', type=str, default='../../private/data/A1/train-topics.list')
    parser.add_argument('-d', metavar='document.list', dest='doc', help='A file with a list of document filenames', type=str, default='../../private/data/A1/documents.list')
    parser.add_argument('-r', metavar='identifier', dest='id', help='A label identifying particular experiment run', type=str, default='Run-0')
    parser.add_argument('-o', metavar='output.dat', dest='output', help='An output file', type=str, default='output.dat')
    parser.add_argument('-c', '--configs', metavar='config_file', nargs='+', dest='configs', help='List of config files', default=['../../ir_config.py'])
    
    args = parser.parse_args()
    config = Config.load_configs(args.configs, use_default=False, log=False)
    data_path = os.path.split(args.doc)[0]
    config['general']['data_path'] = data_path
    config['docid_maker']['CountIDMaker']['document_list_file'] = args.doc
    config['postlist_maker']['FrequencyPostList']['postlist_file']= os.path.join(data_path, 'postlist_result.pkl')

    main()
