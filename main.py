from app.controller.process_controller import ProcessController as pc
import time
import logging
from random import randint

logging.basicConfig(level=logging.INFO)


def task(a, time_to_sleep: int = 2) -> None:
    print(f'Task {a} started with {time_to_sleep} seconds sleep')
    time.sleep(time_to_sleep)
    print(f'Task {a} completed')


if __name__ == '__main__':
    controller = pc(3)
    controller.set_max_proc(3)
    logging.info('Starting the tasks')
    logging.info(f'Running with {controller.max_proc} processes')
    logging.debug('Using DEBUG')
    tasks = [(task, (i, randint(1, 10))) for i in range(20)]
    controller.start(tasks[:10], 0)
    time.sleep(.5)
    controller.start(tasks[10:], )
    print(f'{controller.alive_count()} processes started')
    print(f'{controller.wait_count()} tasks in queue')
    controller.wait()
