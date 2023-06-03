from typing import Any, Optional

from bcsfe.core import game_version, io


class NyankoClub:
    def __init__(
        self,
        officer_id: int,
        total_renewal_times: int,
        start_date: float,
        end_date: float,
        unknown_ts_1: float,
        unknown_ts_2: float,
        start_date_2: float,
        end_date_2: float,
        unknown_ts_3: float,
        flag: int,
        end_date_3: float,
        claimed_rewards: dict[int, int],
        unknown_ts_4: float,
        unknown_bool_1: bool,
        unknown_bool_2: Optional[bool] = None,
    ):
        self.officer_id = officer_id
        self.total_renewal_times = total_renewal_times
        self.start_date = start_date
        self.end_date = end_date
        self.unknown_ts_1 = unknown_ts_1
        self.unknown_ts_2 = unknown_ts_2
        self.start_date_2 = start_date_2
        self.end_date_2 = end_date_2
        self.unknown_ts_3 = unknown_ts_3
        self.flag = flag
        self.end_date_3 = end_date_3
        self.claimed_rewards = claimed_rewards
        self.unknown_ts_4 = unknown_ts_4
        self.unknown_bool_1 = unknown_bool_1
        self.unknown_bool_2 = unknown_bool_2

    @staticmethod
    def read(data: io.data.Data, gv: game_version.GameVersion) -> "NyankoClub":
        officer_id = data.read_int()
        total_renewal_times = data.read_int()
        start_date = data.read_double()
        end_date = data.read_double()
        unknown_ts_1 = data.read_double()
        unknown_ts_2 = data.read_double()
        start_date_2 = data.read_double()
        end_date_2 = data.read_double()
        unknown_ts_3 = data.read_double()
        flag = data.read_int()
        end_date_3 = data.read_double()
        claimed_rewards = data.read_int_int_dict()
        unknown_ts_4 = data.read_double()
        unknown_bool_1 = data.read_bool()
        if gv >= 80100:
            unknown_bool_2 = data.read_bool()
        else:
            unknown_bool_2 = None
        return NyankoClub(
            officer_id,
            total_renewal_times,
            start_date,
            end_date,
            unknown_ts_1,
            unknown_ts_2,
            start_date_2,
            end_date_2,
            unknown_ts_3,
            flag,
            end_date_3,
            claimed_rewards,
            unknown_ts_4,
            unknown_bool_1,
            unknown_bool_2,
        )

    def write(self, data: io.data.Data, gv: game_version.GameVersion):
        data.write_int(self.officer_id)
        data.write_int(self.total_renewal_times)
        data.write_double(self.start_date)
        data.write_double(self.end_date)
        data.write_double(self.unknown_ts_1)
        data.write_double(self.unknown_ts_2)
        data.write_double(self.start_date_2)
        data.write_double(self.end_date_2)
        data.write_double(self.unknown_ts_3)
        data.write_int(self.flag)
        data.write_double(self.end_date_3)
        data.write_int_int_dict(self.claimed_rewards)
        data.write_double(self.unknown_ts_4)
        data.write_bool(self.unknown_bool_1)
        if gv >= 80100:
            data.write_bool(self.unknown_bool_2 or False)

    def serialize(self) -> dict[str, Any]:
        return {
            "officer_id": self.officer_id,
            "total_renewal_times": self.total_renewal_times,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "unknown_ts_1": self.unknown_ts_1,
            "unknown_ts_2": self.unknown_ts_2,
            "start_date_2": self.start_date_2,
            "end_date_2": self.end_date_2,
            "unknown_ts_3": self.unknown_ts_3,
            "flag": self.flag,
            "end_date_3": self.end_date_3,
            "claimed_rewards": self.claimed_rewards,
            "unknown_ts_4": self.unknown_ts_4,
            "unknown_bool_1": self.unknown_bool_1,
            "unknown_bool_2": self.unknown_bool_2,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "NyankoClub":
        return NyankoClub(
            data["officer_id"],
            data["total_renewal_times"],
            data["start_date"],
            data["end_date"],
            data["unknown_ts_1"],
            data["unknown_ts_2"],
            data["start_date_2"],
            data["end_date_2"],
            data["unknown_ts_3"],
            data["flag"],
            data["end_date_3"],
            data["claimed_rewards"],
            data["unknown_ts_4"],
            data["unknown_bool_1"],
            data["unknown_bool_2"],
        )

    def __repr__(self):
        return f"<NyankoClub {self.officer_id}>"

    def __str__(self):
        return f"NyankoClub {self.officer_id}"