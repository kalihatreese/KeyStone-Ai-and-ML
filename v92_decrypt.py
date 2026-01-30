import hashlib, sys, os
from keystone_v92_full_stack import KeystoneVault

def decrypt_vault_file(file_path, master_key_text):
    if not os.path.exists(file_path):
        print("[!] ERROR: File not found.")
        return

    # Derive the same key used for encryption
    master_key = hashlib.sha256(master_key_text.encode()).hexdigest()
    vault = KeystoneVault(master_key)

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = vault.crypt_data(encrypted_data)
    print("\n[V] VERITAS: Vault Content Decrypted:")
    print("-" * 40)
    print(decrypted_data.decode())
    print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] USAGE: python3 v92_decrypt.py <path_to_v92_file>")
        sys.exit(1)
    
    # Static key for this build
    steward_key = "PURCHASE_V92_STEWARDSHIP"
    decrypt_vault_file(sys.argv[1], steward_key)
