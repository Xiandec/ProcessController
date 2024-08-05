import threading
import multiprocessing as mp
import time
import logging


class Starter():
    '''
    Starter class for starting tasks concurrently
    '''
    def control_threads(
            tasks: list[tuple],
            running_tasks: list,
            max_proc: int = 10,
            max_exec_time: int = None) -> None:
        '''
        Start running the tasks concurrently using the specified maximum execution time
        '''
        time_threads = []
        while len(tasks) > 0 or len(running_tasks) > 0:  # check if running or any queued tasks
            for time_thread in time_threads:

                # check if time limit reached
                if max_exec_time is not None and (time.time() - time_thread['time']) > max_exec_time:
                    running_tasks.remove(time_thread['task'])
                    time_threads.remove(time_thread)

                    time_thread['p'].terminate()
                    time_thread['p'].join()
                    logging.debug(f'Process {time_thread['task']} - TL')
                    continue

                # check if threads end work
                if not time_thread['p'].is_alive():
                    running_tasks.remove(time_thread['task'])
                    time_threads.remove(time_thread)

                    time_thread['p'].terminate()
                    time_thread['p'].join()
                    logging.debug(f'Process {time_thread['task']} - END')
                    continue

            time.sleep(.01)  # give other threads a chance to execute

            if len(running_tasks) >= max_proc or len(tasks) == 0:
                continue

            try:
                task = tasks.pop(0)

                process = mp.Process(target=task[0], args=task[1])
                process.start()
                time_threads.append({'p': process,
                                    'time': time.time(),
                                     'task': task})
                running_tasks.append(task)
                logging.debug(f'Process {time_threads[-1]['task']} - START')
            except BaseException as e:
                logging.error(e)

        return


class ProcessController():
    '''
    Process controller for running tasks
    '''

    def __init__(self, max_proc: int = 10) -> None:
        self.max_proc = max_proc
        self.running_tasks = []
        self.tasks = []
        self.starter = None

    def set_max_proc(self, max_proc: int) -> None:
        '''
        Set the maximum number of processes to run concurrently
        '''
        self.max_proc = max_proc
        return

    def start(self, tasks: list[tuple], max_exec_time: int = None) -> None:
        '''
        Start running the tasks concurrently using the specified maximum number of processes
        '''
        self.tasks = tasks
        self.max_exec_time = max_exec_time
        self.starter = threading.Thread(target=Starter.control_threads,
                                        args=(self.tasks,
                                              self.running_tasks,
                                              self.max_proc,
                                              self.max_exec_time))
        self.starter.start()
        logging.debug('Started running tasks')
        return

    def wait_count(self, ) -> int:
        '''
        Return the total number of tasks in queue
        '''
        return len(self.tasks)

    def alive_count(self, ) -> int:
        '''
        Return the number of alive tasks
        '''
        return len(self.running_tasks)

    def wait(self, ) -> None:
        '''
        Wait for all tasks to complete
        '''
        if self.starter is not None and self.starter.is_alive():
            self.starter.join()
        return
