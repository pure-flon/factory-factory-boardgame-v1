"""Game Manager — orchestrates full game lifecycle for boardgame-v1."""

import uuid
from .board import Board


class GameManager:
    """Manages multiple concurrent game sessions.

    Usage:
        gm = GameManager()
        game_id = gm.start_game(num_players=2)
        result = gm.play_turn(game_id)
        status = gm.get_status(game_id)
    """

    def __init__(self):
        self._games: dict[str, Board] = {}

    def start_game(self, num_players: int = 2) -> str:
        """Start a new game session.

        Args:
            num_players: Number of players (default 2).

        Returns:
            game_id: Unique identifier for the new game session.
        """
        if num_players < 1:
            raise ValueError("num_players must be >= 1")
        game_id = str(uuid.uuid4())
        self._games[game_id] = Board(num_players=num_players)
        return game_id

    def play_turn(self, game_id: str) -> dict:
        """Execute one turn for the current player: roll -> move -> check_win.

        Args:
            game_id: Game session identifier returned by start_game().

        Returns:
            TurnResult dict with keys:
                game_id, player_id, steps, old_pos, new_pos, is_win, winner
        """
        board = self._get_board(game_id)
        if board.winner is not None:
            raise RuntimeError(f"Game {game_id} already finished (winner: {board.winner})")
        current = board.current_player()
        result = board.move(current.player_id)
        return {
            "game_id": game_id,
            **result,
            "winner": board.winner,
        }

    def get_status(self, game_id: str) -> dict:
        """Return current state snapshot for a game session.

        Args:
            game_id: Game session identifier.

        Returns:
            Board.state_snapshot() dict with game_id field added.
        """
        board = self._get_board(game_id)
        snapshot = board.state_snapshot()
        snapshot["game_id"] = game_id
        return snapshot

    # ── private ──────────────────────────────────────────────────────────────

    def _get_board(self, game_id: str) -> Board:
        if game_id not in self._games:
            raise KeyError(f"Unknown game_id: {game_id}")
        return self._games[game_id]


if __name__ == "__main__":
    gm = GameManager()
    game_id = gm.start_game(2)
    print(f"Game started: {game_id}")
    print("Initial status:", gm.get_status(game_id))

    for turn in range(30):
        status = gm.get_status(game_id)
        if status["winner"] is not None:
            print(f"\n Player {status['winner']} wins!")
            break
        result = gm.play_turn(game_id)
        print(
            f"Turn {turn + 1}: Player {result['player_id']} rolled {result['steps']}, "
            f"moved {result['old_pos']} -> {result['new_pos']}"
            + (" WIN!" if result["is_win"] else "")
        )
