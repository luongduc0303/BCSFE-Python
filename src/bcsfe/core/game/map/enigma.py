from typing import Any
from bcsfe.core import io


class Stage:
    def __init__(
        self, level: int, stage_id: int, decoding_satus: int, start_time: float
    ):
        self.level = level
        self.stage_id = stage_id
        self.decoding_satus = decoding_satus
        self.start_time = start_time

    @staticmethod
    def init() -> "Stage":
        return Stage(0, 0, 0, 0.0)

    @staticmethod
    def read(data: io.data.Data) -> "Stage":
        level = data.read_int()
        stage_id = data.read_int()
        decoding_satus = data.read_byte()
        start_time = data.read_double()
        return Stage(level, stage_id, decoding_satus, start_time)

    def write(self, data: io.data.Data):
        data.write_int(self.level)
        data.write_int(self.stage_id)
        data.write_byte(self.decoding_satus)
        data.write_double(self.start_time)

    def serialize(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "stage_id": self.stage_id,
            "decoding_satus": self.decoding_satus,
            "start_time": self.start_time,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Stage":
        return Stage(
            data.get("level", 0),
            data.get("stage_id", 0),
            data.get("decoding_satus", 0),
            data.get("start_time", 0.0),
        )

    def __repr__(self):
        return f"Stage({self.level}, {self.stage_id}, {self.decoding_satus}, {self.start_time})"

    def __str__(self):
        return self.__repr__()


class Enigma:
    def __init__(
        self,
        energy_since_1: int,
        energy_since_2: int,
        enigma_level: int,
        unknown_1: int,
        unknown_2: bool,
        stages: list[Stage],
    ):
        self.energy_since_1 = energy_since_1
        self.energy_since_2 = energy_since_2
        self.enigma_level = enigma_level
        self.unknown_1 = unknown_1
        self.unknown_2 = unknown_2
        self.stages = stages

    @staticmethod
    def init() -> "Enigma":
        return Enigma(0, 0, 0, 0, False, [])

    @staticmethod
    def read(data: io.data.Data) -> "Enigma":
        energy_since_1 = data.read_int()
        energy_since_2 = data.read_int()
        enigma_level = data.read_byte()
        unknown_1 = data.read_byte()
        unknown_2 = data.read_bool()
        stages = [Stage.read(data) for _ in range(data.read_byte())]
        return Enigma(
            energy_since_1,
            energy_since_2,
            enigma_level,
            unknown_1,
            unknown_2,
            stages,
        )

    def write(self, data: io.data.Data):
        data.write_int(self.energy_since_1)
        data.write_int(self.energy_since_2)
        data.write_byte(self.enigma_level)
        data.write_byte(self.unknown_1)
        data.write_bool(self.unknown_2)
        data.write_byte(len(self.stages))
        for stage in self.stages:
            stage.write(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "energy_since_1": self.energy_since_1,
            "energy_since_2": self.energy_since_2,
            "enigma_level": self.enigma_level,
            "unknown_1": self.unknown_1,
            "unknown_2": self.unknown_2,
            "stages": [stage.serialize() for stage in self.stages],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Enigma":
        return Enigma(
            data.get("energy_since_1", 0),
            data.get("energy_since_2", 0),
            data.get("enigma_level", 0),
            data.get("unknown_1", 0),
            data.get("unknown_2", False),
            [Stage.deserialize(stage) for stage in data.get("stages", [])],
        )

    def __repr__(self):
        return f"Enigma({self.energy_since_1}, {self.energy_since_2}, {self.enigma_level}, {self.unknown_1}, {self.unknown_2}, {self.stages})"

    def __str__(self):
        return self.__repr__()