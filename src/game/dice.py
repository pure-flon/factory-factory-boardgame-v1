"""Dice roller module — Skills 2.0 task_card output."""

import random


def roll(sides: int = 6) -> int:
    """Roll a single die with given number of sides."""
    return random.randint(1, sides)


def roll_multiple(n: int, sides: int = 6) -> list[int]:
    """Roll n dice, each with given number of sides."""
    return [roll(sides) for _ in range(n)]


if __name__ == "__main__":
    print(roll(), roll_multiple(3))
