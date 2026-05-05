from dataclasses import dataclass

from model.artObject import ArtObject

# classe per rappresentare informazioni al posto di una tupla nel DAO

@dataclass
class Arco:
    o1: ArtObject
    o2: ArtObject
    peso: int