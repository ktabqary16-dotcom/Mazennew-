#!/bin/bash
# Mazennew Installer

echo -e "\033[36m═══════════════════════════════════════════════════════════\033[0m"
echo -e "\033[36m     Mazennew – Installation\033[0m"
echo -e "\033[36m═══════════════════════════════════════════════════════════\033[0m"

# تحديث الحزم
if command -v pkg &> /dev/null; then
    pkg update -y
    pkg install php cloudflared openssh -y
elif command -v apt &> /dev/null; then
    sudo apt update -y
    sudo apt install php cloudflared openssh -y
fi

# تثبيت بايثون
pip install -r requirements.txt

# إنشاء المجلدات
mkdir -p output logs

# إضافة قوائم الكلمات
mkdir -p wordlists
echo -e "admin\nroot\n123456\npassword\ntoor" > wordlists/fast.txt
echo -e "admin\nroot\nuser\ntest\nadministrator" > wordlists/users.txt

chmod +x mazennew.py

echo -e "\033[32m✅ Installation complete!\033[0m"
echo -e "\033[33m🚀 Run: python3 mazennew.py\033[0m"
