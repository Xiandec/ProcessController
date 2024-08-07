from app.controller.process_controller import ProcessController as pc
import time
import logging
from random import randint
from task import task

logging.basicConfig(level=logging.INFO)



if __name__ == '__main__':
    controller = pc(3)
    controller.set_max_proc(3)
    logging.info('Starting the tasks')
    logging.info(f'Running with {controller.get_max_proc()} processes')
    logging.debug('Using DEBUG')
    tasks = [(task, (i, randint(1, 10))) for i in range(20)]
    controller.start(tasks[:10], 1)
    time.sleep(.5)
    controller.start(tasks[10:], 2)
    print(f'{controller.alive_count()} processes started')
    print(f'{controller.wait_count()} tasks in queue')
    #controller.wait()
