import time
import curses
from curses_utils import display_worker_nodes_info
from kube_utils import authenticate_with_kubernetes, get_worker_nodes_info, get_pods_running_on_nodes

def main(stdscr):
    authenticate_with_kubernetes()

    # Setup curses
    curses.curs_set(0)  # Hide cursor
    stdscr.timeout(0)  # Non-blocking input
    stdscr.clear()

    try:
        while True:
            worker_nodes_info = get_worker_nodes_info()
            pods_running_on_nodes = get_pods_running_on_nodes()
            display_worker_nodes_info(stdscr, worker_nodes_info, pods_running_on_nodes)

            # Exit the loop when the user presses 'q'
            key = stdscr.getch()
            if key == ord('q'):
                break

            time.sleep(1) 

    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.addstr(0, 0, "===================================")
        stdscr.addstr(1, 0, "Kubernetes Worker Nodes Overview:")
        stdscr.addstr(2, 0, "===================================")
        stdscr.addstr(4, 0, "You terminated the app with Ctrl+C.")
        stdscr.refresh()
        time.sleep(2) 

if __name__ == "__main__":
    curses.wrapper(main)
