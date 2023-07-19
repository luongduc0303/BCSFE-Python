import random
from typing import Any, Optional
from bcsfe import core
from bcsfe.cli import color


class Upgrade:
    def __init__(self, plus: int, base: int):
        self.plus = plus
        self.base = base

        self.base_range = (0, 0)
        self.plus_range = (0, 0)

    def get_base(self) -> int:
        return self.base + 1

    def get_plus(self) -> int:
        return self.plus

    def upgrade(self):
        self.base += 1

    def increment_base(self, amount: int):
        self.base += amount

    def increment_plus(self, amount: int):
        self.plus += amount

    def get_random_base(self) -> int:
        return random.randint(self.base_range[0], self.base_range[1])

    def get_random_plus(self) -> int:
        return random.randint(self.plus_range[0], self.plus_range[1])

    @staticmethod
    def read(stream: "core.Data") -> "Upgrade":
        plus = stream.read_short()
        base = stream.read_short()

        return Upgrade(plus, base)

    def write(self, stream: "core.Data"):
        stream.write_short(self.plus)
        stream.write_short(self.base)

    def serialize(self) -> dict[str, Any]:
        return {
            "plus": self.plus,
            "base": self.base,
        }

    @staticmethod
    def init() -> "Upgrade":
        return Upgrade(0, 0)

    def reset(self):
        self.plus = 0
        self.base = 0

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Upgrade":
        return Upgrade(data.get("plus", 0), data.get("base", 0))

    def __repr__(self) -> str:
        return f"Upgrade(plus={self.plus}, base={self.base})"

    def __str__(self) -> str:
        return f"Upgrade(plus={self.plus}, base={self.base})"

    @staticmethod
    def get_user_upgrade() -> tuple[Optional["Upgrade"], bool]:
        usr_input = color.ColoredInput().localize("upgrade_input")
        if usr_input == core.local_manager.get_key("quit_key"):
            return None, True
        # example:
        # 10+20 = Upgrade(base=9, plus=20)
        # 10+ = Upgrade(base=9, plus=-1) # -1 means no change
        # +20 = Upgrade(base=-1, plus=20) # -1 means no change
        # 10 = Upgrade(base=9, plus=0)
        # 5-10+20-30 = Upgrade(base=random.randint(4, 9), plus=random.randint(20, 30))
        # 5-10+ = Upgrade(base=random.randint(4, 9), plus=-1)
        # +20-30 = Upgrade(base=-1, plus=random.randint(20, 30))

        parts = usr_input.split("+")
        if len(parts) == 1:
            base = parts[0]
            plus = "0"
        else:
            base = parts[0]
            plus = parts[1]

        min_base, max_base = None, None
        min_plus, max_plus = None, None

        if not base:
            base_int = -1
        else:
            range_parts = base.split("-")
            if len(range_parts) == 1:
                try:
                    min_base = int(range_parts[0]) - 1
                    max_base = min_base
                except ValueError:
                    color.ColoredText.localize("invalid_upgrade_base", base=base)
                    return None, False
            else:
                try:
                    min_base = int(range_parts[0]) - 1
                    max_base = int(range_parts[1]) - 1
                except ValueError:
                    color.ColoredText.localize(
                        "invalid_upgrade_base_random",
                        min=range_parts[0],
                        max=range_parts[1],
                    )
                    return None, False

            base_int = (min_base + max_base) // 2

        if not plus:
            plus_int = -1
        else:
            range_parts = plus.split("-")
            if len(range_parts) == 1:
                try:
                    min_plus = int(range_parts[0])
                    max_plus = min_plus
                except ValueError:
                    color.ColoredText.localize("invalid_upgrade_plus", plus=plus)
                    return None, False
            else:
                try:
                    min_plus = int(range_parts[0])
                    max_plus = int(range_parts[1])
                except ValueError:
                    color.ColoredText.localize(
                        "invalid_upgrade_plus_random",
                        min=range_parts[0],
                        max=range_parts[1],
                    )
                    return None, False

            plus_int = (min_plus + max_plus) // 2

        upgrade = Upgrade(plus_int, base_int)
        upgrade.base_range = (min_base or base_int, max_base or base_int)
        upgrade.plus_range = (min_plus or plus_int, max_plus or plus_int)
        return upgrade, False
