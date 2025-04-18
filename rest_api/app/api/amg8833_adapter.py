from threading import Thread
from threading import Lock
from api.amg8833 import Driver_amg8833
from main.logger import logger
import time



class AMG8833_adapter:
    def __init__(self, rts, pace=1.0):
        self.rts = rts
        self.pace = pace
        try:
            self.amg8833_driver = Driver_amg8833()
        except Exception as e:
            logger.error(f'AMG8833 Driver fault {e}')
        self.lock = Lock()

    def refresh(self):
        try:
            self.lock.acquire()
            response = True
            timestamp = int(time.time() * 1000)
            t_max, t_array, T_thermistor = self.amg8833_driver.read()
            
            self.rts.add('t_max', timestamp, t_max)
            self.rts.add('t_thermistor', timestamp, T_thermistor)

            for row_number,row_data in enumerate(t_array):
                for col_number,cell in enumerate(row_data):
                    self.rts.add(f'array{row_number}{col_number}', timestamp, float(cell))
        except Exception as e:
            logger.error(f'Refresh error {e}')
            response = False
        finally:
            self.lock.release()
            return response
    
    def data_polling(self):
        while True:
            response = self.refresh()
            if response:
                logger.info('Refresh and Polling ok')
            time.sleep(self.pace)