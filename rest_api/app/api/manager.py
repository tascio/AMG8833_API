from api.amg8833_adapter import AMG8833_adapter
from main.logger import logger
import threading



def main(rts):
    try:
        default_pace = 1.0

        amg8833_ad=AMG8833_adapter(rts=rts, pace=default_pace)

        amg8833_thread=threading.Thread(target=amg8833_ad.data_polling,daemon=True)
        amg8833_thread.start()
        logger.info('Thread adapter started')
    except Exception as e:
        logger.critical(f'Error in starting Thread {e}')


