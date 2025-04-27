import itertools

txns = [
    ['Football', 'Jersey'],
    ['Basketball', 'Shoes', 'Jersey'],
    ['Jersey', 'Football', 'Shoes'],
    ['Football', 'Gloves'],
    ['Shoes', 'Basketball', 'Gloves'],
    ['Basketball', 'Football', 'Jersey'],
    ['Football', 'Jersey', 'Shoes', 'Gloves']
]

min_sup = 0.3
num_txns = len(txns)
min_cnt = min_sup * num_txns

u_items = sorted(set(i for t in txns for i in t))

def sup_cnt(iset, ts):
    return sum(1 for t in ts if set(iset).issubset(set(t)))

print("\n--- CANDIDATE & FREQUENT ITEMSETS ---\n")
f_sets = {}
for k in range(1, len(u_items) + 1):
    print(f"\nCandidate {k}-itemsets:")
    cands = {}
    for iset in itertools.combinations(u_items, k):
        s_cnt = sup_cnt(iset, txns)
        cands[iset] = s_cnt
        print(f"{iset}: {s_cnt}")

    freq_k = {iset: cnt for iset, cnt in cands.items() if cnt >= min_cnt}
    if not freq_k:
        break
    f_sets[k] = freq_k

    print(f"\nFrequent {k}-itemsets:")
    for iset, cnt in freq_k.items():
        print(f"{iset}: {cnt}")

print("\n--- FINAL FREQUENT ITEMSETS ---")
for k, isets_k in f_sets.items():
    print(f"\nFrequent {k}-itemsets:")
    for iset, cnt in isets_k.items():
        print(f"{iset}: {cnt}")
