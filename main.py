from AlphaBetaChessTree import AlphaBetaChessTree


def main():
    fen = "4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1"
    chess_tree = AlphaBetaChessTree(fen)
    best = chess_tree.get_best_next_move(fen, 3)

    print("Best move:", best)


if __name__ == "__main__":
    main()
