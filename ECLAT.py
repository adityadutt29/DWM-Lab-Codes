from collections import defaultdict
from itertools import combinations

def run_eclat(txns, min_sup_cnt):
    i_tids = defaultdict(set)
    for tid, tx in enumerate(txns):
        for i in tx:
            i_tids[i].add(tid)

    curr_k_sets = {frozenset({i}): tids for i, tids in i_tids.items() if len(tids) >= min_sup_cnt}
    all_freq_sets = curr_k_sets.copy()
    k = 1

    while curr_k_sets:
        k += 1
        next_k_sets = {}
        prev_k_items = list(curr_k_sets.keys())

        for i in range(len(prev_k_items)):
            for j in range(i + 1, len(prev_k_items)):
                iset1 = prev_k_items[i]
                iset2 = prev_k_items[j]
                
                l1 = sorted(list(iset1))
                l2 = sorted(list(iset2))

                if l1[:-1] == l2[:-1] and l1[-1] < l2[-1]:
                    tids1 = curr_k_sets[iset1]
                    tids2 = curr_k_sets[iset2]
                    n_tids = tids1 & tids2

                    if len(n_tids) >= min_sup_cnt:
                        n_iset = iset1 | iset2
                        next_k_sets[n_iset] = n_tids

        all_freq_sets.update(next_k_sets)
        curr_k_sets = next_k_sets

    return all_freq_sets

txns = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'K', 'E', 'Y'],
    ['C', 'A', 'K', 'E'],
    ['B', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'O', 'K', 'I', 'E']
]

min_sup_cnt = 3

freq_sets_eclat = run_eclat(txns, min_sup_cnt)

print("Frequent Itemsets (ECLAT):")
sorted_freq_sets = sorted(freq_sets_eclat.items(), key=lambda item: len(item[1]), reverse=True)

for iset, tids in sorted_freq_sets:
    print(f" {set(iset)}: {len(tids)}")
