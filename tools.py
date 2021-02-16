def _sum(lst):
    return sum(lst) - 12


def _double(lst):
    return 2 * lst[0] - 6


tools = {
    "Red": [[3], [6], _double],
    "Lite Blue": [[1, 5, 5, 2], [6, 10, 6, 2], _sum],
    "Yellow": [[2, 2, 6, 4], [8, 4, 8, 4, ], _sum],
    "Lavender": [[9, 6], [18, 6], _sum],
    "Green": [[1, 4, 3, 8], [4, 8, 4, 8], _sum],
    "Orange": [[2, 1, 4, 10], [6, 2, 6, 10, ], _sum],
    "Dark Blue": [[6], [6], _double],
    "Brown": [[3, 18], [6, 18], _sum]
}
