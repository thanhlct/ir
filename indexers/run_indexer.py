import pdb

import autopath
from ir.utils.config import Config
from ir.indexers.docid_makers.count_id_maker import CountIDMaker
from ir.indexers.parsers.simple_parser import SimpleParser


def main():
    print 'hello'
    config = Config.load_configs(['../ir_config.py'], use_default=False, log=False)
    id_maker = CountIDMaker(config) 
    id_maker.make_id_from_file()

    parser = SimpleParser(config)
    parser.parse_an_id_maker(id_maker)

if __name__=='__main__':
    main()
