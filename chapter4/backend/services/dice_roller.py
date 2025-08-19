"""A tool for rolling dice."""
import random
from langchain_core.tools import tool

@tool
def roll_dice(dice_string: str) -> str:
    """Rolls a set of dice specified in standard notation (e.g., "1d20", "2d6")."""
    try:
        num_dice, die_type = map(int, dice_string.lower().split('d'))
        if num_dice <= 0 or die_type <= 0:
            return "Please use positive numbers for dice rolls."
        rolls = [random.randint(1, die_type) for _ in range(num_dice)]
        total = sum(rolls)
        return f"Rolling {dice_string}...\nRolls: {', '.join(map(str, rolls))}\nTotal: {total}"
    except ValueError:
        return "Invalid dice notation. Please use the format 'XdY', e.g., '2d6'."
