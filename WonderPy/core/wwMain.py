import threading
import WonderPy


def start(delegate_instance, arguments=None, ws_uri=None):
    if ws_uri:
        WonderPy.core.wwWSMgr.WWWSManager(delegate_instance, arguments, ws_uri).run()
    else:
        WonderPy.core.wwBTLEMgr.WWBTLEManager(delegate_instance, arguments).run()


thread_local_data = threading.local()
