from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

def tick(p):
    print('Tick! The time is: %s' % p)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    tt = datetime.strptime('2016-03-07 12:57:40', "%Y-%m-%d %H:%M:%S")
    scheduler.add_job(tick, 'interval', days=1, next_run_time=tt,args=['ssss'])
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
