#!/usr/bin/python3
'''A script for parsing HTTP request logs.
'''
import re
import sys
import signal

# Global counters
total_file_size = 0
status_codes_stats = {
    '200': 0,
    '301': 0,
    '400': 0,
    '401': 0,
    '403': 0,
    '404': 0,
    '405': 0,
    '500': 0,
}


def extract_input(input_line):
    '''Extracts sections of a line of an HTTP request log.
    '''
    log_pattern = re.compile(
        r'\s*(?P<ip>\S+)\s* - '
        r'\[(?P<date>.*?)\] '
        r'"(?P<request>[^"]*)" '
        r'(?P<status_code>\d{3}) '
        r'(?P<file_size>\d+)'
    )
    match = log_pattern.fullmatch(input_line)
    info = {'status_code': '0', 'file_size': 0}

    if match:
        info['status_code'] = match.group('status_code')
        info['file_size'] = int(match.group('file_size'))
    return info


def update_metrics(line):
    '''Updates the metrics from a given HTTP request log line.
    '''
    global total_file_size
    line_info = extract_input(line)
    status_code = line_info['status_code']
    file_size = line_info['file_size']

    # Update total file size
    total_file_size += file_size

    # Update status code count if it’s one of the expected codes
    if status_code in status_codes_stats:
        status_codes_stats[status_code] += 1


def print_statistics():
    '''Prints the accumulated statistics of the HTTP request log.
    '''
    print("File size: {}".format(total_file_size))
    for code in sorted(status_codes_stats):
        count = status_codes_stats[code]
        if count > 0:
            print("{}: {}".format(code, count))


def signal_handler(sig, frame):
    '''Handles the interrupt signal (CTRL + C) to print statistics.
    '''
    print_statistics()
    sys.exit(0)


def run():
    '''Starts the log parser and processes input line by line.
    '''
    global total_file_size
    line_num = 0

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Process each line of input
    try:
        for line in sys.stdin:
            update_metrics(line)
            line_num += 1

            # Print statistics every 10 lines
            if line_num % 10 == 0:
                print_statistics()
    except EOFError:
        print_statistics()


if __name__ == '__main__':
    run()
