from typing import Literal
from colorama import Back, Fore

from jsontype import Colors


def rgb(
    mode: Literal["fg", "bg", "both"],
    fg: tuple[int, int, int] = (0, 0, 0),
    bg: tuple[int, int, int] = (0, 0, 0),
) -> str:
    fr, fg_, fb = fg
    br, bg_, bb = bg
    if mode == "both":
        return f"\033[38;2;{fr};{fg_};{fb}m\033[48;2;{br};{bg_};{bb}m"
    elif mode == "fg":
        return f"\033[38;2;{fr};{fg_};{fb}m"
    elif mode == "bg":
        return f"\033[48;2;{br};{bg_};{bb}m"


END_MODIFIER: str = "\033[0m"

BASE_COLORS: Colors = {
    "base": Fore.WHITE,
    "lesson": Fore.WHITE,
    "naglowek": Fore.YELLOW,
    "number": Fore.WHITE,
    "room": Fore.WHITE,
    "time": Fore.WHITE,
}

HIGHTLIGHT_DAY: Colors = {
    "base": Fore.LIGHTCYAN_EX,
    "lesson": Fore.BLUE,
    "naglowek": Fore.LIGHTYELLOW_EX,
    "number": Fore.CYAN,
    "room": Fore.LIGHTGREEN_EX,
    "time": Fore.GREEN,
}

_HIGHTLIGHT_COLORS: str = rgb("both", (0, 255, 255), (0, 99, 0))
HIGHTLIGHT_COLORS: Colors = {
    "base": _HIGHTLIGHT_COLORS,
    "lesson": _HIGHTLIGHT_COLORS,
    "naglowek": _HIGHTLIGHT_COLORS,
    "number": _HIGHTLIGHT_COLORS,
    "room": _HIGHTLIGHT_COLORS,
    "time": _HIGHTLIGHT_COLORS,
}

DELETE_MODYFIER: Colors = {
    "base": f"{Back.RED}",
    "lesson": rgb("both", (61, 255, 233), (204, 4, 3)),
    "naglowek": f"{Back.RED}",
    "number": f"{Back.RED}",
    "room": f"{Back.RED}",
    "time": f"{Back.RED}",
}

_CHANGED_MODYFIER: str = rgb("bg", bg=(4, 81, 105))
CHANGED_MODYFIER: Colors = {
    "base": _CHANGED_MODYFIER,
    "lesson": rgb("fg", fg=(0, 255, 37)) + _CHANGED_MODYFIER,
    "naglowek": _CHANGED_MODYFIER,
    "number": _CHANGED_MODYFIER,
    "room": _CHANGED_MODYFIER,
    "time": _CHANGED_MODYFIER,
}
