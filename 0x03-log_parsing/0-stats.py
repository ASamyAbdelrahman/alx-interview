#!/usr/bin/python3
import sys
import re
import signal

# Global variables to store file size and status code counts
file_size = 0
status_counts = {200: 0, 301: 0, 400: 0,
                 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
status_codes = {200, 301, 400, 401, 403, 404, 405, 500}


def signal_handle(sig, frame):
    """Signal handler to print statistics on CTRL + C."""
    print_statistics()
    sys.exit(0)


# Register the signal handler for SIGINT (CTRL + C)
signal.signal(signal.SIGINT, signal_handle)


def check_format(line):
    """Check if the line matches the expected log format and updates metrics."""
    global file_size
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<date>.*?)\] "GET /projects/260 HTTP/1\.1" (?P<status>\d{3}) (?P<size>\d+)$'
    )
    match = log_pattern.match(line)
    if match:
        # Extract data from the line
        status_code = int(match.group('status'))
        size = int(match.group('size'))

        # Update global file size
        file_size += size

        # Update status code count if it’s in the list of valid codes
        if status_code in status_codes:
            status_counts[status_code] += 1
        return True
    return False


def print_statistics():
    """Prints the file size and status code counts."""
    print("File Size: {}".format(file_size))
    for code in sorted(status_counts):
        if status_counts[code] > 0:
            print("{}: {}".format(code, status_counts[code]))


def run():
    count = 0
    for line in sys.stdin:
        if check_format(line):
            count += 1
            # Print every 10 lines
            if count % 10 == 0:
                print_statistics()


if __name__ == '__main__':
    run()
