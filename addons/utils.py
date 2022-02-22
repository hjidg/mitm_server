
import tomli, tomli_w

def ck_dict_to_str(dictitem):
    return '; '.join(['='.join(item) for item in dictitem.items()])

def ck_str_to_dict(string):
    return dict(item.split('=',1) for item in string.split('; '))

def data_str_to_dict(data):
    return dict(item.split('=') for item in data.split('&'))

# 读取toml
def get_toml(path):
    '''
    '''
    with open(path,'rb') as f:
        r = tomli.load(f)
    return r

def save_toml(table,path):
    with open(path,'wb') as f:
        tomli_w.dump(table,f)

def dict2conf(d):
    return ';'.join([f'{k}="{v}"' for k,v in d.items()])