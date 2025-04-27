import itertools

txns = [
    ['apple', 'banana'],
    ['milk', 'bread', 'butter'],
    ['tea', 'sugar'],
    ['apple', 'butter'],
    ['milk', 'cheese', 'apple'],
    ['cheese', 'sugar', 'milk'],
    ['tea', 'bread', 'apple', 'sugar', 'butter']
]

min_sup = 0.3
min_cnt = min_sup * len(txns)

its = sorted(set(i for t in txns for i in t))

def sup_cnt(iset, ts):
    return sum(1 for t in ts if set(iset).issubset(t))

def gen_cands(prev_s, size):
    return [list(set(a) | set(b)) for i, a in enumerate(prev_s)
            for b in prev_s[i+1:] if len(set(a) | set(b)) == size]

freq_sets = {}
k = 1
curr_sets = [[i] for i in its if sup_cnt([i], txns) >= min_cnt]
freq_sets[k] = curr_sets

while curr_sets:
    k += 1
    cands = gen_cands(curr_sets, k)
    v_sets = [c for c in cands if sup_cnt(c, txns) >= min_cnt]
    if not v_sets:
        break
    freq_sets[k] = v_sets
    curr_sets = v_sets

for k, isets in freq_sets.items():
    print(f"\nFrequent {k}-Itemsets:")
    for iset in isets:
        s_count = sup_cnt(iset, txns)
        print(f"{set(iset)} - Support: {s_count}/{len(txns)} ({s_count / len(txns) * 100:.2f}%)")
