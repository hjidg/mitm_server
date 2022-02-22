
from mitmproxy import proxy, options
from mitmproxy.tools.web.master import WebMaster

import glob
from importlib import import_module
import asyncio
from threading import Thread
import queue

def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)
    m.run_loop(loop.run_forever)

def start_webmaster(q_msg,username,password,addon_folder='addons',temp_folder='temp'):
    ex_lst = [f'{addon_folder}/__init__.py',f'{addon_folder}/utils.py']
    addonpys = [item[:-3].replace("/",'.') for item in glob.glob(f'{addon_folder}/*.py') if item not in ex_lst]
    addons = []
    for item in addonpys:
        exec(f'addons.append(import_module(item).{item[7:]}(q_msg,temp_folder))')

    opts = options.Options(
        listen_host='0.0.0.0',
        listen_port=40080,
        confdir='./.mitmproxy',
        ssl_insecure=True,
        add_upstream_certs_to_client_chain=True,
    )
    pconf = proxy.config.ProxyConfig(opts)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    m = WebMaster(options=opts,with_termlog=False)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(*addons)
    m.options.add_option("web_port",int,40081,"")
    m.options.add_option("web_host",str,"0.0.0.0","")
    m.options.update(proxyauth=f"{username}:{password}")
    
    t = Thread(target=loop_in_thread, args=(loop,m))
    return t,m,loop

def mitm_t_start(username,password,addon_folder='addons',temp_folder='temp'):
    q_msg = queue.Queue()
    t,m,loop = start_webmaster(q_msg,username,password,addon_folder,temp_folder)
    return t,m,loop,q_msg

def mitm_t_end(m,loop,q_msg):
    m.shutdown()
    q_msg.put('Done')
    
    