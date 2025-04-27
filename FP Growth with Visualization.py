import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import graphviz
from collections import defaultdict

class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

def build_viz_tree(txns, min_sup_cnt):
    i_counts = defaultdict(int)
    for tx in txns:
        for i in tx: i_counts[i] += 1
    freq_items = {i for i, ct in i_counts.items() if ct >= min_sup_cnt}
    if not freq_items: return None, None
    h_tbl = {i: [i_counts[i], None] for i in freq_items}
    srt_freq_items = sorted(list(freq_items), key=lambda i: h_tbl[i][0], reverse=True)
    i_order = {i: idx for idx, i in enumerate(srt_freq_items)}
    root = FPNode(None, 1, None)
    for tx in txns:
        filt_tx = [i for i in tx if i in freq_items]
        srt_tx = sorted(filt_tx, key=lambda i: i_order[i])
        if srt_tx: ins_tree(srt_tx, root, h_tbl)
    return root, h_tbl

def ins_tree(items, node, h_tbl):
    if not items: return
    f_item = items[0]
    child = node.children.get(f_item)
    if child: child.count += 1
    else:
        child = FPNode(f_item, 1, node)
        node.children[f_item] = child
        upd_link(f_item, child, h_tbl)
    if len(items) > 1: ins_tree(items[1:], child, h_tbl)

def upd_link(item, tgt_node, h_tbl):
    h_info = h_tbl[item]
    curr = h_info[1]
    if curr is None: h_info[1] = tgt_node
    else:
        while curr.node_link is not None: curr = curr.node_link
        curr.node_link = tgt_node

def viz_tree(root, fname='fp_tree_viz'):
    if not root:
        print("Tree empty for viz.")
        return
    dot = graphviz.Digraph(format='png')
    dot.node('rt', 'Root', shape='ellipse')
    q = [(root, 'rt')]
    n_cnt = 0
    while q:
        p_node, p_id = q.pop(0)
        for item, c_node in p_node.children.items():
            n_cnt += 1
            c_id = f'n{n_cnt}'
            n_label = f"{c_node.item}:{c_node.count}"
            dot.node(c_id, n_label, shape='box')
            dot.edge(p_id, c_id)
            q.append((c_node, c_id))
    try:
        dot.render(fname, view=False, cleanup=True)
        print(f"Viz saved: {fname}.png")
    except Exception as e:
         print(f"Viz error: {e}")

txns = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'K', 'E', 'Y'],
    ['C', 'A', 'K', 'E'],
    ['B', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'O', 'K', 'I', 'E']
]

min_sup_cnt = 3
min_sup_rel = min_sup_cnt / len(txns)

te = TransactionEncoder()
te_arr = te.fit(txns).transform(txns)
df = pd.DataFrame(te_arr, columns=te.columns_)

freq_sets_mle = fpgrowth(df, min_support=min_sup_rel, use_colnames=True)

print("Frequent Itemsets (mlxtend):")
print(freq_sets_mle)

viz_root, _ = build_viz_tree(txns, min_sup_cnt)
if viz_root:
    viz_tree(viz_root)
else:
    print("No frequent items for tree viz.")
