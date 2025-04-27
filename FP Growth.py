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

def build_fp_tree(transactions, min_support):
    item_counts = defaultdict(int)
    for tx in transactions:
        for item in tx:
            item_counts[item] += 1

    frequent_items = {item for item, count in item_counts.items() if count >= min_support}
    if not frequent_items:
        return None, None

    header_table = {item: [item_counts[item], None] for item in frequent_items}
    sorted_frequent_items = sorted(list(frequent_items), key=lambda item: header_table[item][0], reverse=True)
    item_order = {item: i for i, item in enumerate(sorted_frequent_items)}

    root_node = FPNode(None, 1, None)

    for tx in transactions:
        filtered_tx = [item for item in tx if item in frequent_items]
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
    head = header_table[item]
    while head[1] is not None:
        head = head[1]
    if isinstance(head, list):
         head[1] = target_node
    else:
        head.node_link = target_node


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
        dot.render(filename, view=False)
        print(f"FP-Tree visualization saved to {filename}.png and {filename}.gv")
    except Exception as e:
         print(f"Could not render visualization. Make sure Graphviz is installed and in your PATH. Error: {e}")


# Example Usage
dataset = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'K', 'E', 'Y'],
    ['M', 'A', 'K', 'E'],
    ['M', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'O', 'K', 'I', 'E']
]

min_support_count = 3

fp_tree_root, header_tbl = build_fp_tree(dataset, min_support_count)

if fp_tree_root:
    visualize_fp_tree(fp_tree_root, filename='my_fp_tree_viz')
else:
    print("No frequent items found for the given minimum support.")
