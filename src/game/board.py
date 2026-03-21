"""Board state machine — E-FACTORY boardgame-v1 core engine."""

from dataclasses import dataclass, field
from typing import Optional
from .dice import roll


BOARD_SIZE = 20  # 총 칸 수 (0=시작, 19=도착)


@dataclass
class Player:
    player_id: int
    position: int = 0
    is_active: bool = True


@dataclass
class Board:
    """보드 상태 관리: 플레이어 위치, 턴 순서, 승리 판정."""

    num_players: int
    players: list[Player] = field(default_factory=list)
    current_turn: int = 0  # index into players
    winner: Optional[int] = None  # player_id of winner, None if game ongoing

    def __post_init__(self):
        if not self.players:
            self.players = [Player(player_id=i) for i in range(self.num_players)]

    # ── public API ─────────────────────────────────────────────────────────

    def move(self, player_id: int, steps: Optional[int] = None) -> dict:
        """주사위 결과에 따른 이동. steps 생략 시 자동 roll().

        Returns:
            dict with keys: player_id, steps, old_pos, new_pos, is_win
        """
        if self.winner is not None:
            raise RuntimeError("Game already finished")

        player = self._get_player(player_id)
        if not player.is_active:
            raise ValueError(f"Player {player_id} is not active")

        if steps is None:
            steps = roll()

        old_pos = player.position
        new_pos = min(old_pos + steps, BOARD_SIZE - 1)
        player.position = new_pos

        is_win = self.check_win(player_id)
        if is_win:
            self.winner = player_id

        self._advance_turn()

        return {
            "player_id": player_id,
            "steps": steps,
            "old_pos": old_pos,
            "new_pos": new_pos,
            "is_win": is_win,
        }

    def check_win(self, player_id: int) -> bool:
        """승리 조건 판정: 마지막 칸(BOARD_SIZE-1) 도달 여부."""
        player = self._get_player(player_id)
        return player.position >= BOARD_SIZE - 1

    def current_player(self) -> Player:
        """현재 턴의 플레이어 반환."""
        return self.players[self.current_turn]

    def state_snapshot(self) -> dict:
        """현재 보드 전체 상태 스냅샷 반환 (UI/직렬화용)."""
        return {
            "num_players": self.num_players,
            "board_size": BOARD_SIZE,
            "current_turn": self.players[self.current_turn].player_id,
            "winner": self.winner,
            "players": [
                {"player_id": p.player_id, "position": p.position, "is_active": p.is_active}
                for p in self.players
            ],
        }

    # ── private helpers ────────────────────────────────────────────────────

    def _get_player(self, player_id: int) -> Player:
        for p in self.players:
            if p.player_id == player_id:
                return p
        raise ValueError(f"Unknown player_id: {player_id}")

    def _advance_turn(self):
        """다음 활성 플레이어로 턴 이동 (게임 종료 시 생략)."""
        if self.winner is not None:
            return
        n = len(self.players)
        for _ in range(n):
            self.current_turn = (self.current_turn + 1) % n
            if self.players[self.current_turn].is_active:
                break

    def __repr__(self) -> str:
        snap = self.state_snapshot()
        lines = [f"Board({self.num_players}p, size={BOARD_SIZE})"]
        for p in snap["players"]:
            marker = "★" if p["player_id"] == snap["current_turn"] else " "
            win_mark = " ← WINNER" if p["player_id"] == snap["winner"] else ""
            lines.append(
                f"  {marker} Player {p['player_id']}: pos={p['position']}/{BOARD_SIZE - 1}{win_mark}"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    board = Board(num_players=2)
    print("Initial state:")
    print(board)

    # 2인 플레이: 각자 5번 이동
    for turn in range(5):
        cp = board.current_player()
        result = board.move(cp.player_id)
        print(f"\nTurn {turn + 1}: Player {result['player_id']} rolled {result['steps']}, "
              f"moved {result['old_pos']} → {result['new_pos']}"
              + (" 🏆 WIN" if result["is_win"] else ""))
        print(board)
        if board.winner is not None:
            break
