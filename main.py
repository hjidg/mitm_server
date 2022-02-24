

from pywebio.session import register_thread,defer_call
from pywebio.input import input,input_group,TEXT,PASSWORD,actions
from pywebio.output import put_buttons,put_text,put_table,use_scope,put_row
from pywebio.pin import put_input,put_select,put_textarea,pin
from pywebio import start_server
import re
import csv
import fcntl
from functools import partial
import queue

from myfunc import get_toml,get_tomls,save_toml,clear_path,add_fixdata
from mitm_utils import mitm_t_start,mitm_t_end
from ql.qlsend import qlsend
from Oreomeow_checkinpanel.make_check import make_check

# 账号操作
def get_account(path='account.csv'):
    '''
    lock file and read account.csv
    '''
    with open(path,'r+') as f:
        fcntl.flock(f.fileno(),fcntl.LOCK_EX)
        reader = csv.reader(f)
        account = {row[0]:row[1] for row in reader}
        lock = account.get('lock')
        if lock=='0':
            account['lock']='1'
            f.seek(0)
            writer = csv.writer(f)
            for row in account.items():
                w = writer.writerow(row)
        return lock,account
def add_account(username,password,account_path='account.csv',toml_folder='tomls'):
    '''
    '''
    with open(account_path,'a+') as f:
        writer = csv.writer(f)
        w = writer.writerow((username,password))
    with open(f'{toml_folder}/{username}.toml','w') as f:
        f.write('\n')
    with open(f'{toml_folder}/{username}.fixtoml','w') as f:
        f.write('\n')
def release_lock(path='account.csv'):
    '''
    '''
    with open(path,'r+') as f:
        fcntl.flock(f.fileno(),fcntl.LOCK_EX)
        reader = csv.reader(f)
        account = {row[0]:row[1] for row in reader}
        account['lock']='0'
        f.seek(0)
        writer = csv.writer(f)
        for row in account.items():
            w = writer.writerow(row)    

# 登录界面
def check_info(info,lock,account):
    '''
    '''
    users = list(account.keys())
    username = info.get('username')
    password = info.get('password')
    is_signup = info.get('action')=='signup'
    is_login = info.get('action')=='login'
    is_edit = info.get('action')=='edit'
    is_cancel = info.get('action')=='cancel'
    if not lock=='0':
        if is_login or is_signup:
            return ('username','资源已被占用，仅编辑模式')
    if not re.match("^[A-Za-z0-9_-]*$",username):
        return ('username','字母数字下划线')
    if not is_cancel:
        if 5>len(username) or len(username)>20:
            return ('username','5-20个字符')
    if is_signup and username in users:
        return ('username','用户已存在')
    if not username in users:
        if is_login or is_edit:
            return ('username','用户不存在')
    if not password==account.get(username):
        if is_login or is_edit:
            return ('password','密码错误')
    if len(password)>20 and not is_cancel:
        return ('password','error: more than 20 letters')
def login_info(lock,account):
    '''
    open a web_page
    '''
    if not lock=='0':
        put_text('资源已被占用，can only edit')
    check_info_par = partial(check_info,lock=lock,account=account)
    info = input_group('首页', [
        input('username', type=TEXT, name='username', required=False),
        input('password', type=PASSWORD, name='password', required=False),
        actions('', [
            {'label': '登录', 'value': 'login'},
            {'label': '注册', 'value': 'signup'},
            {'label': 'Edit', 'value': 'edit'},
            {'label': 'Cancel', 'value': 'cancel', 'color': 'danger'},
        ], name='action', help_text=''),
    ],validate=check_info_par)
    return info

# 用户界面，显示app状态，点击抓包button
def user_page(username,password,toml_folder,addon_folder,temp_folder,all_data_path,qlconf_path):
    '''
    '''
    # show_app_status
    toml_path = f'{toml_folder}/{username}.toml'
    appdata = get_toml(toml_path)
    table = [[item[0],item[1][0].get('_status')] for item in appdata.items()]
    with use_scope('s1',clear=True):
        put_table(table,header=['app','status'])
    # 编辑固定代码和青龙配置
    with open(f'{toml_folder}/{username}.fixtoml','r',encoding='utf-8') as f:
        fixdata = f.read()
    with use_scope('s2',clear=True):
        put_row([
            put_textarea(name='fixdata',label='Fixed Data',rows=13,code={'mode':'markdown'},value=fixdata),
            # put_textarea(name='qldata',label='QL Data',rows=13,code={'mode':'markdown'},value=qldata)
        ])
    # 已经在用的通知方式 字典相同key可以避免重复
    notify_in_use = list({f"{item[1][0].get('_tongzhi_method')}: {item[1][0].get('_tongzhi_param')}":'' for item in appdata.items() if item[1][0].get('_tongzhi_method')}.keys())
    notify_choses = notify_in_use+['New']
    # 
    qlconf = get_toml(qlconf_path)
    ql_in_use = {ql.get('qlremark'):[ql.get('qlurl'),ql.get('qlid'),ql.get('qlsecret')] for ql in qlconf.get('青龙')}
    ql_choses = list(ql_in_use.keys())
    # 写参数
    if ql_choses:
        put_select(label='青龙',options=ql_choses,name='qlc')
    put_select(label='通知',options=notify_choses,name='nc')
    put_select(label='通知方式',options=['bark','qywx'],name='nm')
    put_input(label='通知参数',name='np')
    # 开始抓包
    t,m,loop,q_msg = mitm_t_start(username,password,addon_folder=addon_folder,temp_folder=temp_folder)
    register_thread(t)
    t.setDaemon(True)
    t.start()
    # 按钮
    end_all_par = partial(mitm_t_end,m=m,loop=loop,q_msg=q_msg)
    update_table_par = partial(update_table,appdata=appdata,temp_folder=temp_folder,scope='s1',username=username)
    put_buttons(['renew app status','submit'],onclick=[update_table_par,end_all_par]).show()
    #
    @defer_call
    def on_close():
        m.shutdown()
        release_lock(path=account_path)    
    # 打印log
    with use_scope('log'):
        put_text('Log: ')
    while True:
        # 获取mimtproxy的抓包log
        try:
            a = q_msg.get()
            put_text(a,scope='log')
            q_msg.task_done()
            # 抓包完成，结束
            if a=='Done':
                # temp添加到用户toml
                fixdata = pin['fixdata']
                save_newdata(fixdata,appdata,toml_path,temp_folder,username,pin['nc'],pin['nm'],pin['np'])
                # 清空temp文件夹
                clear_path(temp_folder)
                # 把所有用户toml合并        
                all_data = get_tomls(toml_folder=toml_folder)
                save_toml(all_data,all_data_path)
                # QL
                put_text('capture finished!\n\nstart sending to QL',scope='log')
                if ql_choses:
                    qlurl,qlid,qlsecret = ql_in_use[pin['qlc']]
                    msg = qlsend(all_data_path,qlurl,qlid,qlsecret)
                [put_text(item,scope='log') for item in msg]
                put_text('QL sended!\n',scope='log')
                # checkinpanel
                put_text(make_check(all_data_path),scope='log')
                put_text("\nALL DONE! Just close the window",scope='log')
                break
        except queue.Empty:
            pass
# 合并抓到的toml
def temp2newdata(temp_folder,username,nc,nm,np):
    newdata = get_tomls(toml_folder=temp_folder)
    for app in newdata.keys():
        if nc=='New':
            for i in newdata[app]:
                i['_user'] = username
                i['_tongzhi_method'] = nm
                i['_tongzhi_param'] = np
                i['_status'] = 1
        else:
            for i in newdata[app]:
                nm,np = nc.split(': ')
                i['_user'] = username
                i['_tongzhi_method'] = nm
                i['_tongzhi_param'] = np
                i['_status'] = 1
    return newdata
def update_table(appdata,temp_folder,scope,username):
    newdata = temp2newdata(temp_folder,username,pin['nc'],pin['nm'],pin['np'])
    for item in newdata.keys():
        appdata[item] = newdata[item]
    table = [[item[0],item[1][0].get('_status')] for item in appdata.items()]
    with use_scope(scope,clear=True):
        put_table(table,header=['app','status'])
# 保存抓到的toml
def save_newdata(fixdata,appdata,toml_path,temp_folder,username,nc,nm,np):
    newdata = temp2newdata(temp_folder,username,nc,nm,np)
    for item in newdata.keys():
        appdata[item] = newdata[item]
    save_toml(add_fixdata(fixdata,appdata),toml_path)

def edit_toml(username,toml_folder):
    '''
    '''
    toml_path = f'{toml_folder}/{username}.toml'
    with open(toml_path,'r',encoding='utf-8') as f:
        appdata = f.read()
    with use_scope('toml_edit',clear=True):
        put_row([
            put_textarea(name='appdata',label='App Data',rows=26,code={'mode':'markdown'},value=appdata),
        ])
    def reset_edit():
        with use_scope('toml_edit',clear=True):
            put_row([
                put_textarea(name='appdata',label='App Data',rows=26,code={'mode':'markdown'},value=appdata),
            ])
    def save_edit():
        with open(toml_path,'w',encoding='utf-8') as f:
            fcntl.flock(f.fileno(),fcntl.LOCK_EX)
            f.write(pin['appdata'])
        put_text('saved,just close the window')
    put_buttons(['reset','save'],onclick=[reset_edit,save_edit]).show()
# Main
def task(toml_folder,account_path,all_data_path,addon_folder,temp_folder,qlconf_path):
    '''
    '''
    lock,account = get_account(path=account_path)
    @defer_call
    def on_close():
        if lock=='0':
            release_lock(path=account_path)
    if lock=='0':
        info = login_info(lock,account)
        username = info.get('username')
        password = info.get('password')
        # 点击注册
        if info.get('action')=='signup':
            add_account(username,password,account_path,toml_folder)
            user_page(username,password,toml_folder,addon_folder,temp_folder,all_data_path,qlconf_path)
            release_lock(path='account.csv')
        # 转到用户界面    
        if info.get('action')=='login':
            user_page(username,password,toml_folder,addon_folder,temp_folder,all_data_path,qlconf_path)
            release_lock(path='account.csv')
        # edit
        if info.get('action')=='edit':
            edit_toml(username,toml_folder)
        # 取消登录
        if info.get('action')=='cancel':
            release_lock(path='account.csv')    
    else:
        info = login_info(lock,account)
        username = info.get('username')
        password = info.get('password')
        # edit
        if info.get('action')=='edit':
            edit_toml(username,toml_folder)
        put_text('资源已被占用')

toml_folder = 'tomls'
account_path = 'account.csv'
all_data_path = 'output/all_data.toml'
addon_folder = 'addons'
temp_folder = 'temp'
qlconf_path = 'ql/qlconf.toml'
task_par = partial(task,toml_folder=toml_folder,account_path=account_path,all_data_path=all_data_path,addon_folder=addon_folder,temp_folder=temp_folder,qlconf_path=qlconf_path)

if __name__ == "__main__":
    start_server(
        task_par,
        port=40082,
        debug=True,
        cdn=False,
        auto_open_webbrowser=False,
        remote_access=False,
    )
