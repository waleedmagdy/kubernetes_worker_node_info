import time
import curses
from tabulate import tabulate

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_colored_bar(num_pods, max_pods):
    bar_length = 20
    scaling_factor = bar_length / max_pods if max_pods > 0 else 0
    num_bars = int(num_pods * scaling_factor)

    # Calculate the percentage of pods running
    percentage = int((num_pods / max_pods) * 100)

    # Create the colored bar without ANSI escape codes
    colored_bar = f"[{'#' * num_bars:<{bar_length}}]"
    return f"{colored_bar} ({num_pods}/{max_pods})"

def display_worker_nodes_info(stdscr, worker_nodes_info, pods_running_on_nodes):
    stdscr.clear()
    stdscr.addstr(0, 0, "=================================")
    stdscr.addstr(1, 0, "Kubernetes Worker Nodes Overview:")
    stdscr.addstr(2, 0, "=================================")

    # Get the current time
    current_time = get_current_time()
    stdscr.addstr(3, 0, f"Current Time: {current_time}")

    max_pods = max(pods_running_on_nodes.values(), default=0)

    table_data = []

    for node_info in worker_nodes_info:
        node_name = node_info['node_name']
        cpu_capacity = node_info['cpu_capacity']
        memory_capacity = node_info['memory_capacity']
        storage_capacity = node_info['storage_capacity']
        num_pods = pods_running_on_nodes.get(node_name, 0)

        pod_info = get_colored_bar(num_pods, max_pods)
        table_data.append([current_time, node_name, cpu_capacity, memory_capacity, storage_capacity, pod_info])

    headers = ["Time", "Node Name", "CPU Capacity", "Memory Capacity", "Storage Capacity", "Number of Pods Running"]
    table_str = tabulate(table_data, headers=headers, tablefmt="plain")

    # Split the table string into individual lines
    table_lines = table_str.split('\n')

    # Add each line to the terminal using addstr
    for i, line in enumerate(table_lines):
        stdscr.addstr(5 + i, 0, line, curses.A_BOLD)

    stdscr.refresh()
