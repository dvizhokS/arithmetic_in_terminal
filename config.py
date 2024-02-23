"""
    min_x - minimal first number;
    max_x - maximal first number;
    min_y - minimal second number;
    max_y - maximal second number;
    signs - signs for examples, possible signs( + - / * )
        example:    "signs": "+",
                    "signs": "+-*";
    is_smarty - If you answer an example incorrectly, you need to answer two correctly, possible is_smarty("yes", "no")
        example:    "is_smarty": True (mode enabled),
                    "is_smarty": "False" (mode disabled);
    info_example - Printing information for each example
    example_to_win - number of examples that need to be solved to win
"""

config = {
    "min_x": 0,
    "max_x": 10,
    "min_y": 0,
    "max_y": 10,
    "signs": "+-",
    "is_smarty": True,
    "info_example": False,
    "example_to_win": 10,
}
