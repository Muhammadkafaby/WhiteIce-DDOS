# KeepAlive+NoCache DoS Test Tool

This is a KeepAlive+NoCache DoS Test Tool written in Python. It sends HTTP requests with `Connection: keep-alive` and `Cache-Control: no-cache` headers to a target server using multiple threads.

## Features

- Randomized User-Agent headers to simulate different clients.
- Logging of requests and errors to a specified log file.
- Graceful shutdown on user interruption (Ctrl+C).
- Loading animation to indicate the ongoing attack.
- Menu-driven interface for setting target URL and number of threads.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies using `pip`:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```sh
python

whiteice.py


```

### Menu Options

1. **Start Attack**: Starts the attack on the specified target URL with the configured number of threads.
2. **Set Target URL**: Allows you to set the target URL for the attack.
3. **Set Number of Threads**: Allows you to set the number of concurrent threads for the attack.
4. **Exit**: Exits the program.

### Example

1. Run the script:

   ```sh
   python whiteice.py
   ```

2. Set the target URL:

   ```plaintext
   Enter your choice: 2
   Enter the target URL: http://example.com
   ```

3. Set the number of threads:

   ```plaintext
   Enter your choice: 3
   Enter the number of threads: 200
   ```

4. Start the attack:

   ```plaintext
   Enter your choice: 1
   ```

5. The attack will start, and you will see a loading animation indicating the ongoing attack. To stop the attack, press `Ctrl+C`.

## Important Note

This script is for educational purposes only. Do not use it to attack any website or server without explicit permission from the owner. Unauthorized use of this script may be illegal and unethical.
