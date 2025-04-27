import itertools
from collections import defaultdict, namedtuple
import graphviz

class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

    def display(self, ind=1):
        print('  ' * ind, self.item, ' ', self.count)
        for child in self.children.values():
            child.display(ind + 1)

def build_fp_tree(transactions, min_support):
    item_counts = defaultdict(int)
    for tx in transactions:
        for item in tx:
            item_counts[item] += 1

    frequent_items_support = {item: count for item, count in item_counts.items() if count >= min_support}
    if not frequent_items_support:
        return None, None

    header_table = {item: [count, None] for item, count in frequent_items_support.items()}
    frequent_items_list = sorted(list(frequent_items_support.keys()), key=lambda item: header_table[item][0], reverse=True)
    item_order = {item: i for i, item in enumerate(frequent_items_list)}

    root_node = FPNode(None, 1, None)

    for tx in transactions:
        filtered_tx = [item for item in tx if item in frequent_items_support]
        sorted_tx = sorted(filtered_tx, key=lambda item: item_order[item])
        if sorted_tx:
            insert_tree(sorted_tx, root_node, header_table)

    return root_node, header_table

def insert_tree(items, node, header_table):
    if not items:
        return

    first_item = items[0]
    child = node.children.get(first_item)

    if child:
        child.count += 1
    else:
        child = FPNode(first_item, 1, node)
        node.children[first_item] = child
        update_header_link(first_item, child, header_table)

    if len(items) > 1:
        insert_tree(items[1:], child, header_table)

def update_header_link(item, target_node, header_table):
    head_info = header_table[item]
    current = head_info[1]
    if current is None:
        head_info[1] = target_node
    else:
        while current.node_link is not None:
            current = current.node_link
        current.node_link = target_node


def ascend_tree(node):
    path = []
    while node.parent is not None and node.parent.item is not None:
        path.append(node.parent.item)
        node = node.parent
    return path[::-1]

def find_prefix_paths(base_item, header_table):
    conditional_patterns = []
    node = header_table[base_item][1]
    while node is not None:
        prefix_path = ascend_tree(node)
        if prefix_path:
            conditional_patterns.append((prefix_path, node.count))
        node = node.node_link
    return conditional_patterns

def mine_fp_tree(header_table, min_support, prefix, frequent_itemsets):
    sorted_items = sorted(list(header_table.keys()), key=lambda item: header_table[item][0])

    for item in sorted_items:
        new_frequent_set = prefix.copy()
        new_frequent_set.add(item)
        support = header_table[item][0]
        frequent_itemsets[frozenset(new_frequent_set)] = support

        conditional_pattern_bases = find_prefix_paths(item, header_table)
        conditional_transactions = []
        for path, count in conditional_pattern_bases:
            for _ in range(count):
                conditional_transactions.append(path)

        conditional_tree_root, conditional_header = build_fp_tree(conditional_transactions, min_support)

        if conditional_header:
            mine_fp_tree(conditional_header, min_support, new_frequent_set, frequent_itemsets)


def visualize_fp_tree(root_node, filename='fp_tree'):
    if not root_node:
        print("Tree is empty.")
        return

    dot = graphviz.Digraph(comment='FP-Tree', format='png')
    dot.node('root', 'Root', shape='ellipse')

    q = [(root_node, 'root')]
    node_count = 0

    while q:
        parent_node, parent_id_str = q.pop(0)
        for item, child_node in parent_node.children.items():
            node_count += 1
            child_id_str = f'node{node_count}'
            node_label = f"{child_node.item}:{child_node.count}"
            dot.node(child_id_str, node_label, shape='box')
            dot.edge(parent_id_str, child_id_str)
            q.append((child_node, child_id_str))

    try:
        dot.render(filename, view=False, cleanup=True)
        print(f"FP-Tree visualization saved to {filename}.png")
    except Exception as e:
         print(f"Could not render visualization. Make sure Graphviz is installed and in your PATH. Error: {e}")

dataset = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'K', 'E', 'Y'],
    ['C', 'A', 'K', 'E'],
    ['B', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'O', 'K', 'I', 'E']
]

min_support_count = 3
frequent_itemsets_result = {}

fp_tree_root, header_tbl = build_fp_tree(dataset, min_support_count)

if fp_tree_root and header_tbl:
    mine_fp_tree(header_tbl, min_support_count, set(), frequent_itemsets_result)
    visualize_fp_tree(fp_tree_root, filename='my_fp_tree_viz_with_mining')

    print("\nFrequent Itemsets (Itemset: Support Count):")
    sorted_frequent_itemsets = sorted(frequent_itemsets_result.items(), key=lambda item: item[1], reverse=True)
    for itemset, support in sorted_frequent_itemsets:
        print(f" {set(itemset)}: {support}")

else:
    print("No frequent items found for the given minimum support.")
