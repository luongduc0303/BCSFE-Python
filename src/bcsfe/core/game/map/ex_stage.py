from typing import Any
from bcsfe.core import io


class Stage:
    def __init__(self, clear_amount: int):
        self.clear_amount = clear_amount

    @staticmethod
    def read(stream: io.data.Data) -> "Stage":
        clear_amount = stream.read_int()
        return Stage(clear_amount)

    def write(self, stream: io.data.Data):
        stream.write_int(self.clear_amount)

    def serialize(self) -> dict[str, Any]:
        return {"clear_amount": self.clear_amount}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Stage":
        return Stage(data["clear_amount"])

    def __repr__(self) -> str:
        return f"Stage(clear_amount={self.clear_amount!r})"

    def __str__(self) -> str:
        return f"Stage(clear_amount={self.clear_amount!r})"


class Chapter:
    def __init__(self, stages: list[Stage]):
        self.stages = stages

    @staticmethod
    def read(stream: io.data.Data) -> "Chapter":
        total = 12
        stages: list[Stage] = []
        for _ in range(total):
            stages.append(Stage.read(stream))
        return Chapter(stages)

    def write(self, stream: io.data.Data):
        for stage in self.stages:
            stage.write(stream)

    def serialize(self) -> dict[str, list[dict[str, Any]]]:
        return {"stages": [stage.serialize() for stage in self.stages]}

    @staticmethod
    def deserialize(data: dict[str, list[dict[str, Any]]]) -> "Chapter":
        return Chapter([Stage.deserialize(stage) for stage in data["stages"]])

    def __repr__(self) -> str:
        return f"Chapter(stages={self.stages!r})"

    def __str__(self) -> str:
        return f"Chapter(stages={self.stages!r})"


class Chapters:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    @staticmethod
    def read(stream: io.data.Data) -> "Chapters":
        total = stream.read_int()
        chapters: list[Chapter] = []
        for _ in range(total):
            chapters.append(Chapter.read(stream))

        return Chapters(chapters)

    def write(self, stream: io.data.Data):
        stream.write_int(len(self.chapters))
        for chapter in self.chapters:
            chapter.write(stream)

    def serialize(self) -> dict[str, list[dict[str, Any]]]:
        return {"chapters": [chapter.serialize() for chapter in self.chapters]}

    @staticmethod
    def deserialize(data: dict[str, list[dict[str, Any]]]) -> "Chapters":
        return Chapters([Chapter.deserialize(chapter) for chapter in data["chapters"]])

    def __repr__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"

    def __str__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"