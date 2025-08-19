"""A simple dice roller service."""
import random
import re


def roll_dice_sync(dice_string: str) -> str:
    """
    Rolls dice based on a standard dice notation string (e.g., '2d6', '1d20+5').

    Args:
        dice_string: The dice notation string.

    Returns:
        The result of the dice roll as a string.
    """
    try:
        # Regex to parse the dice string, e.g., "2d6+3"
        match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_string.lower().strip())
        if not match:
            return "Invalid dice format. Please use a format like '2d6' or '1d20+3'."

        num_dice = int(match.group(1))
        num_sides = int(match.group(2))
        modifier_str = match.group(3)

        modifier = 0
        if modifier_str:
            modifier = int(modifier_str)

        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        if modifier != 0:
            return f"Rolled {rolls} + {modifier} = {total}"
        return f"Rolled {rolls} = {total}"

    except Exception as e:
        return f"Error rolling dice: {e}"
