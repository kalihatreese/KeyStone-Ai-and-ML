import sys
import numpy as np
import pandas as pd
from internal.veritas.forensic_engine import VeritasAuditor
from internal.veritas.report_generator import VeritasReporter
from internal.sharpe.strategy_engine import SharpeStrategist
from internal.keystone.arbiter_engine import KeystoneArbiter
from internal.keystone.payment_listener import KeystoneListener
from internal.keystone.ingest_engine import KeystoneIngest

class KeystoneV92Core:
    def __init__(self, tx_hash=None):
        self.listener = KeystoneListener()
        if not self.listener.trigger_vault_sequence(tx_hash if tx_hash else ""):
            print("[!] CRITICAL: ACCESS DENIED. VALID STEWARDSHIP REQUIRED.")
            sys.exit(1)
            
        self.ingest = KeystoneIngest()
        self.veritas = VeritasAuditor()
        self.reporter = VeritasReporter()
        self.sharpe = SharpeStrategist()
        self.keystone = KeystoneArbiter()

    def execute_full_cycle(self):
        # 1. INGEST
        payload_path = self.ingest.scan_for_payload()
        if not payload_path:
            print("[!] ABORT: No healthcare payload found in data_intake/.")
            return

        raw_data = self.ingest.parse_to_tensor(payload_path)
        
        # 2. VERITAS (Audit)
        entropy_mask = self.veritas.scan_for_entropy(raw_data)
        entropy_coeff = np.sum(entropy_mask) / len(raw_data)
        
        # 3. SHARPE (Optimize)
        efficiency = self.sharpe.optimize_recovery(0, entropy_coeff, 500)
        
        # 4. KEYSTONE (Validate)
        aligned, resonance = self.keystone.validate_alignment(entropy_coeff, "Healthcare_Sector_Audit")
        
        if aligned:
            # 5. REPORT (Proof of Work)
            report_path = self.reporter.generate_proof_of_work(
                payload_path, entropy_mask, efficiency, resonance
            )
            print(f"========================================")
            print(f"[V] CYCLE COMPLETE: THE MOUNTAIN HAS SPOKEN.")
            print(f"[V] RESONANCE: {resonance:.4f}")
            print(f"========================================")
        else:
            print("[!] KEYSTONE: Resonance below 0.92 floor. Audit discarded.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] USAGE: python3 trinity_control.py <TX_HASH>")
        sys.exit(1)

    v92 = KeystoneV92Core(tx_hash=sys.argv[1])
    v92.execute_full_cycle()
