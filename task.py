import time
def task(a, time_to_sleep: int = 2) -> None:
    print(f'Task {a} started with {time_to_sleep} seconds sleep')
    time.sleep(time_to_sleep)
    print(f'Task {a} completed')