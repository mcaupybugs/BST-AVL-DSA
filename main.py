import re


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # For AVL tree


class BST:
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def preorder(self, root):
        return [root.key] + self.preorder(root.left) + self.preorder(root.right) if root else []


class AVL:
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def preorder(self, root):
        return [root.key] + self.preorder(root.left) + self.preorder(root.right) if root else []


# Helper Functions

def read_input(filename):
    with open(filename, 'r') as file:
        content = file.read()
        
    acceptances_week1 = re.findall(r'\[(.*?)\]', content)[0].split(', ')
    acceptances_week1 = [int(x) for x in acceptances_week1]

    new_acceptances_week2 = re.findall(r'\[(.*?)\]', content)[1].split(', ')
    new_acceptances_week2 = [int(x) for x in new_acceptances_week2]

    declines_week2 = re.findall(r'\[(.*?)\]', content)[2].split(', ')
    declines_week2 = [int(x) for x in declines_week2]

    return acceptances_week1, new_acceptances_week2, declines_week2



def write_output(filename, output_lines):
    with open(filename, 'w') as file:
        for line in output_lines:
            file.write(line + "\n")


def find_coordinates(root, key, level=0, position=0):
    if not root:
        return None
    if root.key == key:
        return level, position
    left = find_coordinates(root.left, key, level + 1, position)
    if left:
        return left
    return find_coordinates(root.right, key, level + 1, position + (1 << level))


def main():
    input_file = "inputPS03.txt"
    output_file = "OutputPS03.txt"
    week1_acceptances, week2_acceptances, declines = read_input(input_file)

    bst = BST()
    avl = AVL()

    bst_root = None
    avl_root = None

    # Insert week 1 acceptances
    for num in week1_acceptances:
        bst_root = bst.insert(bst_root, num)
        avl_root = avl.insert(avl_root, num)

    output_lines = []
    output_lines.append("End of week 1 - Acceptances")
    output_lines.append(f"Preorder traversal of the constructed BST tree is {bst.preorder(bst_root)}")
    output_lines.append(f"Preorder traversal of the constructed AVL tree is {avl.preorder(avl_root)}")

    # Insert week 2 acceptances
    for num in week2_acceptances:
        bst_root = bst.insert(bst_root, num)
        avl_root = avl.insert(avl_root, num)

    output_lines.append("End of week 2 – With new acceptances")
    output_lines.append(f"Preorder traversal of the rearranged BST tree is {bst.preorder(bst_root)}")
    output_lines.append(f"Preorder traversal of the re-arranged AVL tree is {avl.preorder(avl_root)}")

    # Remove declines
    for num in declines:
        bst_root = bst.delete(bst_root, num)
        avl_root = avl.delete(avl_root, num)

    output_lines.append("End of week 2 – After declines")
    output_lines.append(f"Preorder traversal of the rearranged BST tree is {bst.preorder(bst_root)}")
    output_lines.append(f"Preorder traversal of the re-arranged AVL tree is {avl.preorder(avl_root)}")

    # Randomly select three members from the final list
    import random
    final_accepted = bst.preorder(bst_root)  # Same list for both BST and AVL since content is identical
    volunteers = random.sample(final_accepted, 3)
    output_lines.append(f"Randomly selected three volunteers = {volunteers}")
    output_lines.append("BST:")
    for volunteer in volunteers:
        level, position = find_coordinates(bst_root, volunteer)
        output_lines.append(f"Employee # {volunteer} is present in level {level} and its position is {position} from the left.")

    output_lines.append("AVL:")
    volunteers = random.sample(final_accepted, 3)
    for volunteer in volunteers:
        level, position = find_coordinates(avl_root, volunteer)
        output_lines.append(f"Employee # {volunteer} is present in level {level} and its position is {position} from the left.")
    write_output(output_file, output_lines)


if __name__ == "__main__":
    main()
