class TreeNode:
    def __init__(self, board, turn):
        self._board = board
        self._turn = turn
        self._score = None
        self._children = []

    def add_child(self, child):
        self._children.append(child)

