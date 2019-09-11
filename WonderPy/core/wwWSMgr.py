

import queue
import asyncio
import json
import logging
import threading
import websockets
from .wwRobot import WWRobot
from .wwHAL import WWHAL
from .wwConstants import WWRobotConstants
from WonderPy.core import wwMain

# logging.basicConfig(level=logging.DEBUG)

class WWWSManager(WWHAL):
    def __init__(self, delegate, arguments, uri):
        logging.info('WWWSManager.__init__()...')
        print('WWWSManager.__init__()...')
        super().__init__(delegate)
        self._delegate = delegate
        self._arguments = arguments
        self._uri = uri

        logging.info('WWWSManager.__init__()...done')

    def run(self):
        logging.info('WWWSManager.run()')
        self.robot = WWRobot( WWRobotConstants.RobotType.WW_ROBOT_DASH )
        self.robot._sendJson = self.sendJson

        # Start the robot task in another thread
        self._robot_thread = threading.Thread(target=self.robot_thread)
        self._robot_thread.start()

        # Connect to the remote websocket server and start the tasks
        # asyncio.run(self._ws_client_task())
        # asyncio.get_event_loop().run_until_complete(self._ws_client_task())
        ws_thread_loop = asyncio.new_event_loop()
        self._ws_out_queue = asyncio.Queue(loop=ws_thread_loop)
        ws_thread = threading.Thread(target=self._ws_thread, args=(ws_thread_loop,))
        ws_thread.start()

        if hasattr(self.delegate, 'on_connect') and callable(getattr(self.delegate, 'on_connect')):
            wwMain.thread_local_data.in_on_connect = True
            self.delegate.on_connect(self.robot)
            wwMain.thread_local_data.in_on_connect = False

        ws_thread.join()

    def sendJson(self, dict):
        if (len(dict) == 0):
            return
        json_str = json.dumps(dict)
        logging.debug('Send JSON: {}'.format(json_str))
        self._ws_out_queue.put_nowait(json_str)
  
    def robot_thread(self):
        logging.info('Robot thread started.')
        while True:
            # Parse sensor packets, if any
            # This is a coroutine; we should not block here
            try:
                jsonDict = self._sensor_queue.get(block=False)
                self.robot._parse_sensors(jsonDict)
                if hasattr(self.delegate, 'on_sensors') and callable(getattr(self.delegate, 'on_sensors')):
                    wwMain.thread_local_data.in_on_sensors = True
                    self.delegate.on_sensors(self.robot)
                    wwMain.thread_local_data.in_on_sensors = False

            except queue.Empty:
                pass

            # Send any staged robot commands
            self.robot.send_staged()

    def _ws_thread(self, loop):
        # loop = asyncio.new_event_loop()
        logging.info('Starting _ws_client_task()...')
        loop.run_until_complete(self._ws_client_task())
        logging.info('Starting _ws_client_task()...done')

    async def _ws_client_task(self):
        logging.info('Connecting to WS server...')
        async with websockets.connect(self._uri) as websocket:
            logging.info('Connected to WS server: {}'.format(self._uri))
            producer_task = asyncio.ensure_future(self._producer_task(websocket))
            consumer_task = asyncio.ensure_future(self._consumer_task(websocket))
            done, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()

    async def _producer_task(self, websocket):
        while True:
            msg = await self._ws_out_queue.get()
            await websocket.send(msg)

    async def _consumer_task(self, websocket):
        # Receive sensor packets here
        async for message in websocket:
            self._sensor_queue.put(json.loads(message))
