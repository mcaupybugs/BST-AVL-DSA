import random

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # For AVL Tree

# Function to insert nodes in BST
def insert_bst(root, key):
    if not root:
        return TreeNode(key)
    if key < root.value:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root

# Function to insert nodes in AVL Tree
def insert_avl(root, key):
    # Standard BST insertion
    if not root:
        return TreeNode(key)
    if key < root.value:
        root.left = insert_avl(root.left, key)
    else:
        root.right = insert_avl(root.right, key)
    
    # Update height of the ancestor node
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    
    # Get the balance factor
    balance = get_balance(root)
    
    # Balance the tree
    # Left Left Case
    if balance > 1 and key < root.left.value:
        return right_rotate(root)
    
    # Right Right Case
    if balance < -1 and key > root.right.value:
        return left_rotate(root)
    
    # Left Right Case
    if balance > 1 and key > root.left.value:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    
    # Right Left Case
    if balance < -1 and key < root.right.value:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    
    return root

def left_rotate(z):
    y = z.right
    T2 = y.left
    
    # Perform rotation
    y.left = z
    z.right = T2
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    # Return the new root
    return y

def right_rotate(z):
    y = z.left
    T3 = y.right
    
    # Perform rotation
    y.right = z
    z.left = T3
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    # Return the new root
    return y

def get_height(root):
    if not root:
        return 0
    return root.height

def get_balance(root):
    if not root:
        return 0
    return get_height(root.left) - get_height(root.right)

# Function for pre-order traversal
def pre_order_traversal(root):
    return [root.value] + pre_order_traversal(root.left) + pre_order_traversal(root.right) if root else []

# Function to remove a node from the BST or AVL
def remove_node(root, key):
    if not root:
        return root
    
    if key < root.value:
        root.left = remove_node(root.left, key)
    elif key > root.value:
        root.right = remove_node(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        
        temp = get_min_value_node(root.right)
        root.value = temp.value
        root.right = remove_node(root.right, temp.value)
    
    if not root:
        return root
    
    # Update the height of the current node
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    
    # Check the balance factor and balance the tree
    balance = get_balance(root)
    
    # Balance the tree
    if balance > 1 and get_balance(root.left) >= 0:
        return right_rotate(root)
    
    if balance > 1 and get_balance(root.left) < 0:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    
    if balance < -1 and get_balance(root.right) <= 0:
        return left_rotate(root)
    
    if balance < -1 and get_balance(root.right) > 0:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    
    return root

def get_min_value_node(root):
    if root is None or root.left is None:
        return root
    return get_min_value_node(root.left)

# Function to find the coordinates of a node in the tree
def find_coordinates(root, key):
    queue = [(root, 0, 0)]
    while queue:
        node, level, pos = queue.pop(0)
        if node.value == key:
            return level, pos
        if node.left:
            queue.append((node.left, level + 1, pos * 2))
        if node.right:
            queue.append((node.right, level + 1, pos * 2 + 1))
    return None

# Read input from file
with open('inputPS03.txt', 'r') as file:
    lines = file.readlines()
    acceptances_week_1 = set(map(int, lines[0].split()))
    new_acceptances_week_2 = set(map(int, lines[1].split()))
    declines_week_2 = set(map(int, lines[2].split()))

# Initial BST and AVL trees with acceptances of week 1
bst_root = None
avl_root = None
for emp in acceptances_week_1:
    bst_root = insert_bst(bst_root, emp)
    avl_root = insert_avl(avl_root, emp)

# Output pre-order traversal of BST and AVL after week 1
bst_pre_order_week_1 = pre_order_traversal(bst_root)
avl_pre_order_week_1 = pre_order_traversal(avl_root)

# Insert new acceptances of week 2
for emp in new_acceptances_week_2:
    bst_root = insert_bst(bst_root, emp)
    avl_root = insert_avl(avl_root, emp)

# Output pre-order traversal of BST and AVL after inserting new acceptances
bst_pre_order_acceptance = pre_order_traversal(bst_root)
avl_pre_order_acceptance = pre_order_traversal(avl_root)

# Remove declines from the trees
for emp in declines_week_2:
    bst_root = remove_node(bst_root, emp)
    avl_root = remove_node(avl_root, emp)

# Output pre-order traversal of BST and AVL after removing declines
bst_pre_order_final = pre_order_traversal(bst_root)
avl_pre_order_final = pre_order_traversal(avl_root)

# Randomly select three employees from the final list
final_employees = list(acceptances_week_1.union(new_acceptances_week_2) - declines_week_2)
selected_employees = random.sample(final_employees, 3)

# Find coordinates of selected employees
coordinates = {}
for emp in selected_employees:
    coordinates[emp] = find_coordinates(avl_root, emp)

# Write output to file
with open('OutputPS03.txt', 'w') as file:
    file.write("Pre-order traversal of BST and AVL tree after week 1:\n")
    file.write(f"BST: {bst_pre_order_week_1}\n")
    file.write(f"AVL: {avl_pre_order_week_1}\n\n")
    file.write("Pre-order traversal of BST and AVL tree after new acceptances in week 2:\n")
    file.write(f"BST: {bst_pre_order_acceptance}\n")
    file.write(f"AVL: {avl_pre_order_acceptance}\n\n")
    file.write("Pre-order traversal of BST and AVL tree after removing declines:\n")
    file.write(f"BST: {bst_pre_order_final}\n")
    file.write(f"AVL: {avl_pre_order_final}\n\n")
    for emp, (level, pos) in coordinates.items():
        file.write(f"Employee #{emp} is present in level {level} and its position is {pos} from the left.\n")

# Performance comparison between BST and AVL tree (Optional: This should be documented in report)
