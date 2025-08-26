# 🕷️ botnet

**An educational Python-based simulation of a basic botnet crypto miner.**  
This project is designed for ethical hacking education, red team training, and cybersecurity awareness. It demonstrates how a command-and-control (C2) structure can remotely control a miner across compromised machines — without causing real harm.

> ❗ This is **not real malware** and does **not perform unauthorized access or harm**. It is a safe, contained, and legal simulation meant for learning purposes only.

---

## 📚 What This Project Demonstrates

- Remote command-and-control (C2) over TCP
- Downloading and launching a miner (XMRig)
- Adding persistence to Windows startup
- System resource monitoring using built-in tools
- Controlling miner CPU usage (e.g., limit to 60%)
- A basic socket-based bot/client structure

---

## ⚙️ Setup Instructions

### Requirements

- Windows OS (tested on Windows 10/11)
- Python 3.7+
- Internet connection (for downloading XMRig)
- A basic TCP server (for control commands)

> ✅ No external libraries like `psutil` are used — all functionality is implemented with built-in Python modules.

### 1. Clone the repo

```bash
~/ git clone https://github.com/yourusername/botnet
~/ cd botnet
```
### 2. Start C2 Server
- You can use a simple Python script or even nc (Netcat) to simulate a controller OR use the C2 from the repo.

```bash

~/ python c2.py
```

This will:

- Start listening on 127.0.0.1:9999

- Accept multiple bot connections

- Display logs and bot messages

- Allow you to type and broadcast commands to all connected bots

### 3. Run the Bot (Victim Simulation)  
On the target machine (or local test VM):
```bash
~/ python bot.py
```

This connects to a C2 server listening on 127.0.0.1:9999 by default. You can change the IP and port in the script.

### Supported Commands: 

| Command          | Description                                   |
| ---------------- | --------------------------------------------- |
| `download_xmrig` | Downloads and extracts the XMRig miner        |
| `start_xmrig`    | Starts the miner (limited to \~60% CPU usage) |
| `stop_mining`    | Stops the mining process                      |
| `report_status`  | Returns current CPU and memory usage          |
| `persist`        | Adds the bot script to Windows startup        |
| `exit`           | Gracefully terminates the bot                 |


### This project is created strictly for educational, research, and cybersecurity training purposes.

> 🧠 Do not run this code on machines you do not own or without explicit permission.

> 🧪 Only use in controlled lab environments, such as:

- Cybersecurity classrooms

- CTF challenges

- Malware analysis sandboxes

- Red team/blue team simulations

> ❌ We do not support, encourage, or tolerate malicious use.

> ⚖️ Unauthorized use may violate local, state, or international laws.

> The authors of this project are not responsible for any misuse.
