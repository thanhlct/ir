import gzip
import codecs
import copy

def read_gz_file(path):
    zf = gzip.open(path, 'rb')
    contents = zf.read()
    zf.close()
    return contents

def read_gz_text_file(path, encoding='utf-8'):
    '''wont be used, since it return a reader, and not support close'''
    reader = codecs.getreader(encoding)
    contents = read_gz_file(path)
    contents = reader(contents)
    #contents = contents.decode(encoding)#the same as above line
    return contents

def gz_text_file_line_iter(path, encoding='utf-8'):
    zf = gzip.open(path, 'rb')
    reader = codecs.getreader(encoding)
    contents = reader(zf)
    for line in contents.readlines():
        yield line
    zf.close()

def deep_copy(o):
    return copy.deepcopy(o)
