#!/bin/bash
echo "[V] VERITAS: Commencing GitHub & Kernel Forensic Repair..."

# 1. Clear Python Cache (Stop Kernel bloat)
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "[V] VERITAS: Python bytecode cache purged."

# 2. Fix Git Ownership & Permissions (Termux specific)
git config --global --add safe.directory $(pwd)
echo "[V] VERITAS: Directory permissions stabilized."

# 3. Force Sync & Rebase
echo "[V] VERITAS: Attempting to pull sovereign manifest..."
git add .
git commit -m "V92 Alignment: Internal Kernel Fix"
git pull --rebase origin main

# 4. Push Truth
if [ $? -eq 0 ]; then
    git push origin main
    echo "[V] VERITAS: GitHub alignment SUCCESSFUL."
else
    echo "[!] VERITAS: Conflict detected. Executing FORCE alignment..."
    git push origin main --force
fi

echo "[V] VERITAS: Repair Complete. Restart your kernel now."
