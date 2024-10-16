# ANScanner
---
![111111111](logo1.webp)

ANScanner is an advanced network scanning tool designed for use in the Termux environment. This tool allows users to efficiently scan IP ranges and domains to identify active hosts, check open ports, and detect operating systems. Built using pure Python, ANScanner leverages `nmap` for scanning capabilities while providing a user-friendly interface styled with the `rich` library for enhanced terminal output.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

## Features

- **Host Discovery**: Quickly identify active hosts in a given IP range or domain.
- **Port Scanning**: Scan common ports (1-1024) to check for open services.
- **Operating System Detection**: Identify the operating system of the discovered hosts.
- **Rich Terminal UI**: Enhanced output using the `rich` library for a better user experience.
- **Progress Feedback**: Real-time feedback during scanning to ensure users are informed of the process.
- **Error Handling**: Robust error handling to deal with invalid inputs and scanning issues.

## Installation

To install and run ANScanner, follow these steps:

1. **Install Termux**: Ensure you have Termux installed on your Android device. You can download it from the [Google Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/packages/com.termux/).

2. **Install Required Packages**:
   Open Termux and run the following commands to install Python and `nmap`:
```bash
   pkg update
   pkg upgrade
   pkg install python
   pkg install nmap
   pip install rich pyfiglet
```

3. **Clone the Repository**:
   Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/rkstudio585/ANScanner.git
   cd ANScanner
   ```

4. **Run the Tool**:
   You can run the scanner by executing:
   ```bash
   python main.py
   ```

## Usage

Once you run the tool, you will be prompted to enter an IP range or domain. Here are a few examples of input formats:

- To scan an IP range:
  ```ip
  192.168.1
  ```
- To scan a specific domain:
  ```url
  example.com
  ```

### Example Session

```plaintext
Enter the IP range or domain (e.g., 192.168.1 or example.com): example.com
Scanning... Please wait...
Active hosts found: 1
IP Address        Open Ports           Operating System
--------------------------------------------------------
142.250.182.142   None                 Linux
```

## How It Works

1. **Input Handling**: The user inputs an IP range or domain. The tool attempts to resolve the input. If the input is a valid domain, it resolves to its IP address. Otherwise, it defaults to scanning the specified local IP range.

2. **Network Scanning**:
   - The tool utilizes the `nmap` command to perform a ping scan (`-sn`) to discover active hosts in the specified range.
   - Once active hosts are identified, it proceeds to scan common ports (1-1024) on each host to check for open services.
   - The tool also detects the operating system of each active host using the `nmap` OS detection feature (`-O`).

3. **Output Display**: The results are displayed in a formatted table using the `rich` library, providing a clear overview of active hosts, their open ports, and detected operating systems.

## Contributing

Contributions to ANScanner are welcome! If you have suggestions for improvements, bug fixes, or new features, please create a pull request or open an issue in the repository.

---
