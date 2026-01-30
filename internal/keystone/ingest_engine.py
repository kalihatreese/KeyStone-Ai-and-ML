import os
import pandas as pd
import numpy as np

class KeystoneIngest:
    def __init__(self, intake_dir="data_intake"):
        self.intake_dir = intake_dir
        if not os.path.exists(self.intake_dir):
            os.makedirs(self.intake_dir)
            print(f"[V] INGEST: Created Silo Intake at ./{self.intake_dir}")

    def scan_for_payload(self):
        files = [f for f in os.listdir(self.intake_dir) if f.endswith('.csv')]
        if not files:
            return None
        print(f"[V] INGEST: Found {len(files)} payload(s). Processing first entry: {files[0]}")
        return os.path.join(self.intake_dir, files[0])

    def parse_to_tensor(self, file_path):
        """
        Converts raw CSV healthcare data into a mathematical tensor 
        for Veritas to audit.
        """
        try:
            df = pd.read_csv(file_path)
            # Architect Note: We only extract numerical features for the engine
            data_tensor = df.select_dtypes(include=[np.number]).values
            return data_tensor
        except Exception as e:
            print(f"[!] INGEST ERROR: Failed to parse payload. {e}")
            return None

if __name__ == "__main__":
    ingest = KeystoneIngest()
    payload = ingest.scan_for_payload()
    if not payload:
        print("[V] INGEST: Intake silo empty. Awaiting sector data.")
