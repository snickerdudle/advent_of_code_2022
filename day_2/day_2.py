"""Day 2."""
from typing import Sequence

#             R       P       S       R       P       S
incentive = {'X': 1, 'Y': 2, 'Z': 3, 'A': 1, 'B': 2, 'C': 3}


def get_outcome(they: str, you: str) -> int:
  they_p, you_p = incentive[they], incentive[you]
  if (they_p + 3 - you_p) % 3 == 0:
    # Draw
    return 3
  elif (they_p + 3 - you_p) % 3 == 1:
    # Lose
    return 0
  elif (they_p + 3 - you_p) % 3 == 2:
    # Win
    return 6


def get_data() -> Sequence[Sequence[str]]:
  with open('day_2.txt', 'r') as f:
    data = f.read().strip().split('\n')
    data = [i.strip().split(' ') for i in data]
  return data


def part_1() -> None:
  # First, get the data
  data = get_data()
  total_score = 0
  for they, you in data:
    result = get_outcome(they, you)
    total_score += result + incentive[you]
  return total_score


def part_2() -> None:
  # First, get the data
  data = get_data()
  # X lose, Y draw, Z win
  your_choices = ['X', 'Y', 'Z']
  outcome_offset = {'X': -1, 'Y': 0, 'Z': 1}
  total_score = 0
  for they, outcome in data:
    # Based on the outcome, we get the necessary offset
    offset = outcome_offset[outcome]
    your_choice = your_choices[(incentive[they] - 1 + offset + 3) % 3]
    print(they, your_choice, outcome)
    total_score += (3 + 3 * outcome_offset[outcome]) + incentive[your_choice]
  return total_score


if __name__ == '__main__':
  print(part_1())
  print(part_2())
