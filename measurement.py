import time
import psutil


# to start a test
# including time, memory, disk i/o
def measure_start():
    start_time = time.time()
    process = psutil.Process()
    start_memory = process.memory_info().rss
    start_disk_io = psutil.disk_io_counters().read_bytes
    return start_time, start_memory, start_disk_io


# to end a test
# including time, memory, disk i/o as measure_start()
def measure_end():
    end_time = time.time()
    process = psutil.Process()
    end_memory = process.memory_info().rss
    end_disk_io = psutil.disk_io_counters().read_bytes
    return end_time, end_memory, end_disk_io


# print results
def measure_output(start, end):
    # calculation
    time_cost = end[0] - start[0]
    memory_cost = end[1] - start[1]
    disk_io = end[2] - start[2]
    # print format
    print(f"Time cost: {time_cost} seconds")
    print(f"Memory cost: {memory_cost} bytes")
    print(f"Disk I/O: {disk_io} bytes")


# print title
def print_title(task, query, method):
    print(f"Evaluating Task {task}, query: {query}, using {method} algorithm")
