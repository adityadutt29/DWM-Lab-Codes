import itertools
from collections import defaultdict

def apriori(transactions, min_support):
    item_counts = defaultdict(int)
    for tx in transactions:
        for item in tx:
            item_counts[frozenset([item])] += 1

    num_tx = float(len(transactions))
    L = []
    support_data = {}

    L1 = set()
    for itemset, count in item_counts.items():
        support = count / num_tx
        if support >= min_support:
            L1.add(itemset)
            support_data[itemset] = support
    L.append(L1)

    k = 2
    while L[k-2]:
        Lk_1 = L[k-2]
        Ck = set()
        
        items_in_Lk_1 = sorted(list(Lk_1))
        for i in range(len(items_in_Lk_1)):
             for j in range(i + 1, len(items_in_Lk_1)):
                 item1 = items_in_Lk_1[i]
                 item2 = items_in_Lk_1[j]
                 if sorted(list(item1))[:k-2] == sorted(list(item2))[:k-2]:
                      candidate = item1.union(item2)
                      if len(candidate) == k:
                           all_subsets_frequent = True
                           for subset in itertools.combinations(candidate, k - 1):
                               if frozenset(subset) not in Lk_1:
                                   all_subsets_frequent = False
                                   break
                           if all_subsets_frequent:
                               Ck.add(candidate)

        candidate_counts = defaultdict(int)
        for tx in transactions:
            tx_set = set(tx)
            for candidate in Ck:
                if candidate.issubset(tx_set):
                    candidate_counts[candidate] += 1

        Lk = set()
        for itemset, count in candidate_counts.items():
            support = count / num_tx
            if support >= min_support:
                Lk.add(itemset)
                support_data[itemset] = support

        if not Lk:
            break
        L.append(Lk)
        k += 1

    all_frequent_itemsets = set().union(*L)
    return all_frequent_itemsets, support_data
