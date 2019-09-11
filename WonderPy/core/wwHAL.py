import ctypes
import json
import os
import queue

from WonderPy.config import WW_ROOT_DIR

def string_into_c_byte_array(str, cba):
    n = 0
    for c in str:
        cba[n] = ord(c)
        n += 1

class WWHAL:
    def __init__(self, delegate):
        self.delegate = delegate

        self._load_HAL()

        self.robot = None

        self._sensor_queue = queue.Queue()

    def _load_HAL(self):
        import platform
        if platform.system() == 'Darwin':
            HAL_path = os.path.join(WW_ROOT_DIR, 'lib/WonderWorkshop/osx/libWWHAL.dylib')
        elif platform.system() == 'Linux':
            HAL_path = os.path.join(WW_ROOT_DIR, 'lib/WonderWorkshop/linux_x64/libWWHAL.so')
        else:
            raise Exception('Platform not supported: {}'.format(system.platform))
        self.libHAL = ctypes.cdll.LoadLibrary(HAL_path)
        self.libHAL.packets2Json.restype  = (ctypes.c_char_p)

    def sendJson(self, dict):
        raise NotImplementedError('Implement/override me!')
