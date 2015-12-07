import pdb

import autopath
from ir.utils.config import Config

def main():
    print 'hello'
    config = Config.load_configs(['ir_config.py'], use_default=False, log=False)

if __name__=='__main__':
    main()
