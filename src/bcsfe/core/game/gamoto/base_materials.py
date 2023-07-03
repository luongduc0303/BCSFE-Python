from bcsfe.core import io, game, country_code
from bcsfe.cli import dialog_creator


class Material:
    def __init__(self, amount: int):
        self.amount = amount

    @staticmethod
    def init() -> "Material":
        return Material(0)

    @staticmethod
    def read(stream: io.data.Data) -> "Material":
        amount = stream.read_int()
        return Material(amount)

    def write(self, stream: io.data.Data):
        stream.write_int(self.amount)

    def serialize(self) -> int:
        return self.amount

    @staticmethod
    def deserialize(data: int) -> "Material":
        return Material(data)

    def __repr__(self) -> str:
        return f"Material(amount={self.amount!r})"

    def __str__(self) -> str:
        return self.__repr__()


class Materials:
    def __init__(self, materials: list[Material]):
        self.materials = materials

    @staticmethod
    def init() -> "Materials":
        return Materials([])

    @staticmethod
    def read(stream: io.data.Data) -> "Materials":
        total = stream.read_int()
        materials: list[Material] = []
        for _ in range(total):
            materials.append(Material.read(stream))
        return Materials(materials)

    def write(self, stream: io.data.Data):
        stream.write_int(len(self.materials))
        for material in self.materials:
            material.write(stream)

    def serialize(self) -> list[int]:
        return [material.serialize() for material in self.materials]

    @staticmethod
    def deserialize(data: list[int]) -> "Materials":
        return Materials([Material.deserialize(material) for material in data])

    def __repr__(self) -> str:
        return f"Materials(materials={self.materials!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def edit_base_materials(self, cc: "country_code.CountryCode"):
        names = game.catbase.gatya_item.GatyaItemNames(cc).names
        items = game.catbase.gatya_item.GatyaItemBuy(cc).get_by_category(7)
        names = [names[item.id] for item in items]
        base_materials = [base_material.amount for base_material in self.materials]
        values = dialog_creator.MultiEditor.from_reduced(
            "base_materials",
            names,
            base_materials,
            9999,
            group_name_localized=True,
        ).edit()
        self.materials = [Material(value) for value in values]