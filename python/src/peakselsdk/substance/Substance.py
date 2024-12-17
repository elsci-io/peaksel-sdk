import json

from peakselsdk.util.dict_util import entity_to_dict


class SubstanceChem:
    """
    Contains chemical props like MF and the mass, is used to create a substance.
    """
    def __init__(self, emw: float = None, mf: str = None, color: str = None,
                 structureId: str = None, alias: str = None, **kwargs):
        """
        Depending on which chem information you have (EMW, MF or structure like SMILES/MOL/SDF/InChi) you need
        to fill that particular field when submitting the substance. The API will then calculate the rest of the
        fields if possible.

        :param structureId: to get it you first need to submit a structure as an attachment, and pass that ID here
        """
        chem_fields = [emw, mf, structureId]
        if chem_fields.count(None) == len(chem_fields):
            raise Exception(f"At least one of the fields must not be null: emw, mf, structureId")
        self.structureId: str | None = structureId
        self.color: str | None = color
        self.alias: str | None = alias
        self.mf: str | None = mf
        self.emw: float = emw

    @staticmethod
    def from_json(json: dict) -> "SubstanceChem":
        return SubstanceChem(**json)

    def to_json_fields(self) -> dict[str, any]:
        return entity_to_dict(self)

    def __str__(self):
        return json.dumps(self.to_json_fields())


class Substance(SubstanceChem):
    def __init__(self, substance: SubstanceChem, id: str, structureSvgPath: str = None, **kwargs):
        self.__dict__.update(substance.__dict__)
        self.eid: str = id
        self.structureSvgPath: str | None = structureSvgPath # exists only if structure (like SMILES) is present

    @staticmethod
    def from_json(json: dict) -> "Substance":
        return Substance(SubstanceChem.from_json(json), **json)

    @staticmethod
    def from_jsons(jsons: list[dict]) -> list["Substance"]:
        substances: list[Substance] = []
        for substance in jsons:
            substances.append(Substance.from_json(substance))
        return substances

    def to_json_fields(self) -> dict[str, any]:
        return entity_to_dict(self, {"eid": "id"})