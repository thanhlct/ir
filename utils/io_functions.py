'''
Support Functions about input, output
'''

import cPickle as pickle
import copy_reg, types
import os

def object_to_file(obj, fname):
    #register_instancemethod()
    with open(fname, 'wb') as f:
        pickle.dump(obj, f, -1)#protocl 0 default-text-based; binary mode for1,2 and set -1, HIGHGEST PROTOCOL is normal???

def file_to_object(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)

def register_instancemethod():
    copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

def file_exists(path):
    return isfile(path)

def isfile(path):
    return os.path.isfile(path)
