import time, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
import amg8833_i2c
import numpy as np


class Driver_amg8833:
    def __init__(self):
        self.pix_to_read = 64
        # Sensor Init
        self.t0 = time.time()
        self.sensor = []
        while (time.time() - self.t0) < 1:  # wait 1sec for sensor to start
            try:
                self.sensor = amg8833_i2c.AMG8833(addr=0x69)  # start AMG8833
            except:
                self.sensor = amg8833_i2c.AMG8833(addr=0x68)
            finally:
                pass
        time.sleep(0.3)  # wait for sensor to settle

        if not self.sensor:
            print("No AMG8833 Found - Check Your Wiring")
            sys.exit()

    def read(self):
        # read sensor data
        status, pixels = self.sensor.read_temp(self.pix_to_read)
        t_max = max(pixels)
        t_array = np.array(pixels).reshape(8, 8)
        T_thermistor = self.sensor.read_thermistor()

        # print('Thermistor: ', T_thermistor)
        # print('All Pixels :\n', t_array)
        # print('Max temp° => ', t_max)

        # for row_number,row_data in enumerate(t_array):
        #     for col_number,cell in enumerate(row_data):
        #         print(f'riga: {row_number}, colonna: {col_number}, cella: {cell}')

        return t_max, t_array, T_thermistor


driver = Driver_amg8833()
driver.read()


