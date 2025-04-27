import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth

txns = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'K', 'E', 'Y'],
    ['M', 'A', 'K', 'E'],
    ['M', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'O', 'K', 'I', 'E']
]

# Minimum Support
min_sup_cnt = 3
min_sup_rel = min_sup_cnt / len(txns)

# Data Transformation
te = TransactionEncoder()
te_arr = te.fit(txns).transform(txns)
df = pd.DataFrame(te_arr, columns=te.columns_)

# FP-Growth Execution
freq_sets = fpgrowth(df, min_support=min_sup_rel, use_colnames=True)

print("Frequent Itemsets (FP-Growth using mlxtend):")
print(freq_sets)
