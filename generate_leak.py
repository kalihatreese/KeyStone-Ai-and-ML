import pandas as pd
import numpy as np
import os

# Create the silo intake if missing
os.makedirs("data_intake", exist_ok=True)

# Generate 1,000 rows of sector data
# Features: [Billing_Amount, Days_to_Pay, Error_Code, Provider_Rank, Insurance_Friction]
np.random.seed(92) 
rows = 1000
data = {
    'Billing_Amount': np.random.uniform(1000, 50000, rows),
    'Days_to_Pay': np.random.randint(15, 180, rows),
    'Error_Code': np.random.choice([0, 1], size=rows, p=[0.72, 0.28]), # 28% Entropy
    'Provider_Rank': np.random.uniform(0, 1, rows),
    'Insurance_Friction': np.random.uniform(0, 100, rows)
}

df = pd.DataFrame(data)
df.to_csv("data_intake/healthcare_leak_v92.csv", index=False)
print("[V] VERITAS: Generated payload 'healthcare_leak_v92.csv' in data_intake.")
