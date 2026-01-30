import json
import uuid
from datetime import datetime

class KeystoneInvoice:
    def __init__(self, amount_usd, client_id):
        self.invoice_id = str(uuid.uuid4())[:8]
        self.amount = amount_usd
        self.client = client_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_paypal_link(self):
        # Format for a standard PayPal.me request link
        return f"https://www.paypal.com/paypalme/keystoneaiml/{self.amount}USD"

    def generate_crypto_payload(self):
        # Placeholder for Keystone Crypto Lock (Specify your BTC/USDT/ETH wallet)
        return {
            "wallet": "YOUR_WALLET_ADDRESS_HERE",
            "amount_crypto": f"FIXED_RATE_CONVERSION",
            "memo": f"V92_SUBSCRIPTION_{self.invoice_id}"
        }

    def manifest(self):
        data = {
            "system": "Keystone Alignment Model V92",
            "invoice": self.invoice_id,
            "client": self.client,
            "fiat_usd": self.amount,
            "paypal_link": self.generate_paypal_link(),
            "crypto": self.generate_crypto_payload(),
            "status": "UNPAID",
            "resonance_check": "V27_VALIDATED"
        }
        return json.dumps(data, indent=4)

if __name__ == "__main__":
    # Example: $500 Subscription for Client_001
    invoice = KeystoneInvoice(500, "RESIDENT_BETA_01")
    print(f"[V] SENTINEL: NEW INVOICE GENERATED\n{invoice.manifest()}")
