import os, sys, hashlib, binascii
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# PHASE II: THE VAULT (SOVEREIGN XOR STREAM)
# ==========================================
class KeystoneVault:
    def __init__(self, master_key_hex):
        # Stretch the key to 64 bytes for the stream cipher
        self.key = hashlib.sha512(master_key_hex.encode()).digest()
        
    def crypt_data(self, data):
        """Pure Python XOR Cipher: Zero Dependencies."""
        if isinstance(data, str): data = data.encode()
        key_len = len(self.key)
        return bytes([b ^ self.key[i % key_len] for i, b in enumerate(data)])

# ==========================================
# PHASE III: THE REVENUE (INVOICE GEN)
# ==========================================
class KeystoneInvoice:
    def generate(self, recovery_amount, client_id):
        fee = recovery_amount * 0.15
        inv_id = f"INV-{client_id}-{int(datetime.now().timestamp())}"
        content = f"KEYSTONE V92 INVOICE\nID: {inv_id}\nRECOVERY: ${recovery_amount:,.2f}\nFEE: ${fee:,.2f}"
        return inv_id, content

# ==========================================
# THE TRINITY CONSOLIDATION
# ==========================================
class TrinityV92:
    def __init__(self, key_hex):
        self.vault = KeystoneVault(key_hex)
        self.invoice = KeystoneInvoice()
        
    def execute_all_phases(self, payload_path):
        print(f"[V] TRINITY: Executing Sovereign Stack for {payload_path}")
        if not os.path.exists(payload_path):
            print(f"[!] ERROR: {payload_path} not found. Running simulation.")
            df = pd.DataFrame({
                'Billing_Amount': np.random.uniform(1000, 50000, 100),
                'Error_Code': np.random.choice([0, 1], 100)
            })
        else:
            df = pd.read_csv(payload_path)

        leaked = df[df['Error_Code'] == 1]
        val = leaked['Billing_Amount'].sum()
        
        # Vaulting (Encryption)
        report_txt = f"V92 Audit: {len(leaked)} leaks. Total: ${val:,.2f}"
        encrypted = self.vault.crypt_data(report_txt)
        
        # Invoicing
        inv_id, inv_txt = self.invoice.generate(val, "SECTOR-0")
        
        # Write to local silos
        with open(f"vault/{inv_id}.v92", "wb") as f: f.write(encrypted)
        with open(f"invoices/{inv_id}.txt", "w") as f: f.write(inv_txt)
        
        print(f"========================================")
        print(f"[V] SUCCESS: Vaulted Report & Invoice Created.")
        print(f"[V] INVOICE ID: {inv_id}")
        print(f"========================================")

if __name__ == "__main__":
    # Ensure silos exist
    os.makedirs("vault", exist_ok=True)
    os.makedirs("invoices", exist_ok=True)
    
    # Generate Stewardship Key
    master_key = hashlib.sha256(b"PURCHASE_V92_STEWARDSHIP").hexdigest()
    trinity = TrinityV92(master_key)
    trinity.execute_all_phases("data_intake/healthcare_leak_v92.csv")
