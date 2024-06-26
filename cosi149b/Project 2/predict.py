import pandas as pd
import numpy as np
import pickle as pkl

df_test = pd.read_pickle("test.pkl")
length = len(df_test)

output = pd.Series("FALSE" for i in range(0, length))

i = 0
t = 0
for note in df_test:
    if len(note) > 50000:
        output[i] = "TRUE"
        t += 1
    i += 1

print(t/2045)
output.to_csv("test_result.csv")