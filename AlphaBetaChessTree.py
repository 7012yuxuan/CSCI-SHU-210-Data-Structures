from TreeNode import TreeNode
import chess
import networkx as nx
import matplotlib.pyplot as plt


class AlphaBetaChessTree:
    def __init__(self, fen):

        self.board = chess.Board(fen)

    @staticmethod
    def get_supported_evaluations():

        return ["simple_material_evaluation"]

    def _apply_move(self, move, node, notation="SAN"):

        new_board = node._board.copy()
        new_board.push_san(move)
        new_node = TreeNode(new_board, not node._turn)
        node.add_child(new_node)

    def _get_legal_moves(self, node, notation="SAN"):

        return [node._board.san(move) for move in node._board.legal_moves]

    def get_best_next_move(self, fen, depth, notation="SAN"):

        root_board = chess.Board(fen)
        root_node = TreeNode(root_board, root_board.turn)

        best_move = None
        best_score = float('-inf')
        for move in self._get_legal_moves(root_node, notation):
            self._apply_move(move, root_node)
            score = self._alpha_beta(root_node._children[-1], depth - 1, float('-inf'), float('inf'),
                                     not root_node._turn)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _alpha_beta(self, node, depth, alpha, beta, maximizing_player):

        if depth == 0 or node._board.is_game_over():
            return self._evaluate_position(node, depth)

        if maximizing_player:
            value = float('-inf')
            for move in self._get_legal_moves(node):
                self._apply_move(move, node)
                value = max(value, self._alpha_beta(node._children[-1], depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in self._get_legal_moves(node):
                self._apply_move(move, node)
                value = min(value, self._alpha_beta(node._children[-1], depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def _evaluate_position(self, node, depth):

        return self._evaluate_board(node._board)

    def _evaluate_board(self, board):

        # Implement a simple material evaluation
        score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            score += len(board.pieces(piece_type, chess.WHITE)) * self._get_piece_value(piece_type)
            score -= len(board.pieces(piece_type, chess.BLACK)) * self._get_piece_value(piece_type)
        return score

    def _get_piece_value(self, piece_type):

        if piece_type == chess.PAWN:
            return 1
        elif piece_type == chess.KNIGHT:
            return 3
        elif piece_type == chess.BISHOP:
            return 3
        elif piece_type == chess.ROOK:
            return 5
        elif piece_type == chess.QUEEN:
            return 9
        else:  # King
            return 0

    def get_board_visualization(self, board):

        return board.unicode()

    def visualize_decision_process(self, depth, move, notation="SAN"):

        root = self.board.copy()
        root.push_san(move)
        root_node = TreeNode(root, not self.board.turn)
        self._build_tree(root_node, depth - 1)

        G = nx.DiGraph()
        self._construct_graph(G, root_node)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=8)
        plt.show()

    def _build_tree(self, node, depth):
        if depth == 0 or node._board.is_game_over():
            return

        for move in self._get_legal_moves(node):
            self._apply_move(move, node)
            self._build_tree(node.children[-1], depth - 1)

    def _construct_graph(self, G, node):
        G.add_node(node._board.fen(), label=f"Score: {self._evaluate_board(node._board)}")
        for child in node._children:
            G.add_edge(node._board.fen(), child._board.fen())
            self._construct_graph(G, child)

    def export_analysis(self):
        analysis = {}
        analysis["move_evaluations"] = self._get_move_evaluations(self.board, 3)
        analysis["pruned_nodes"] = self.pruned_nodes
        analysis["explored_nodes"] = self.explored_nodes
        analysis["search_depth"] = self.search_depth

        # Save the analysis dictionary to a file
        with open("analysis.txt", "w") as f:
            for key, value in analysis.items():
                f.write(f"{key}: {value}\n")

    def _get_move_evaluations(self, node, depth):
        move_evaluations = {}
        for move in self._get_legal_moves(node):
            self._apply_move(move, node)
            score = self._alpha_beta(node.children[-1], depth - 1, float('-inf'), float('inf'), not node._turn)
            move_evaluations[move.san()] = score
        return move_evaluations
