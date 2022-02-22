
import tomli
import glob, os
import fcntl

import tomli_w

# 读取toml
def get_toml(path):
    '''
    '''
    with open(path,'rb') as f:
        r = tomli.load(f)
    return r

def get_tomls(toml_folder='tomls'):
    '''
    '''
    path_lst = glob.glob(f"{toml_folder}/*.toml")
    f_lst = [open(path,'r',encoding='utf-8') for path in path_lst]
    lines_lst = [f.read() for f in f_lst]
    [f.close() for f in f_lst]
    res = '\n'.join(lines_lst)
    return tomli.loads(res)

def save_toml(data,path):
    with open(path,'wb') as f:
        fcntl.flock(f.fileno(),fcntl.LOCK_EX)
        w  = tomli_w.dump(data,f)

def clear_path(path):
    for file in glob.glob(f"{path}/*"):
        os.remove(file)

def add_fixdata(fixdata,appdata):
    fixdict = {k:v[0] for k,v in tomli.loads(fixdata).items()}
    apps = fixdict.keys()
    for app in apps:
        if app in appdata.keys():
            for item in appdata[app]:
                item.update(fixdict[app])
    return appdata
