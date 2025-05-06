class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedListFixed:
    """
    A fixed version of a doubly linked list that supports node insertion, manual linking,
    and cycle-safe forward traversal.

    This implementation allows for the possibility of circular links (e.g., tail.next = head),
    and the `traverse` method is safeguarded against infinite loops by detecting such cycles.

    Attributes:
        head (Node): The first node in the list.
        tail (Node): The last node in the list.
    """

    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None
        self.tail = None

    def add_node(self, data):
        """
        Append a new node with the given data to the end of the list.

        Args:
            data: The value to store in the new node.

        Returns:
            Node: The newly created node.
        """
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return new_node

    def link_nodes(self, node1, node2):
        """
        Manually link two nodes in the list, connecting node1 to node2.

        This method sets:
            node1.next = node2
            node2.prev = node1

        Warning:
            This method does not validate or update the head or tail references.
            It can introduce cycles, which are handled by the traverse method.

        Args:
            node1 (Node): The node that will point to node2.
            node2 (Node): The node that will point back to node1.
        """
        node1.next = node2
        node2.prev = node1

    def traverse(self):
        """
        Traverse the list from head to tail, collecting all visited nodes.

        If a cycle is detected (i.e., revisiting the head), the traversal stops.

        Returns:
            List[Node]: A list of visited nodes in order.
        """
        visited = []
        current = self.head
        while current:
            visited.append(current)
            current = current.next
            if current == self.head:
                break
        return visited

if __name__ == '__main__':
    dll = DoublyLinkedListFixed()
    n1 = dll.add_node(10)
    n2 = dll.add_node(20)
    n3 = dll.add_node(30)

    # # Manually linking (optional, since add_node already links them)
    # dll.link_nodes(n1, n2)
    # dll.link_nodes(n2, n3)

    # Traverse and print the values
    for node in dll.traverse():
        print(
            f'Node data: {node.data}, Prev: {node.prev.data if node.prev else None}, Next: {node.next.data if node.next else None}')
