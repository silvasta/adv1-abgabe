import re

class Datensatz:
    def __init__(self, input):
        self.input = input
        id, rest = input.split("= ")
        self.datensatzId = re.sub("[^0-9]", "", id)
        self.ifcEntity, rest = rest.split("(",1)
        self.datenfeldliste = rest[:-3]

    def __repr__(self):
        return "DatensatzID = {} -|- Entität = {} -|- Datenfeldliste = {}".format(self.datensatzId, self.ifcEntity, self.datenfeldliste)

    def parse_datenfeldliste(self):
        if self.ifcEntity == "IFCPROPERTYSET":
            self.datenfeldliste = self.datenfeldliste.split(",",4)
            self.datenfeldliste[4] = self.datenfeldliste[4][2:-1].split(",#")
        if self.ifcEntity == "IFCPROPERTYSINGLEVALUE":
            self.datenfeldliste = self.datenfeldliste.split(",")

class IfcSlab(Datensatz):
    def __init__(self, input):
        super().__init__(input)
        self.datenfeldliste = self.datenfeldliste.split(",")

class IfcRelDefinesbyProperties(Datensatz):
    def __init__(self, input):
        super().__init__(input)
        self.datenfeldliste = self.datenfeldliste.split(",")
        self.datenfeldliste[4] = re.sub("[^0-9]", "", self.datenfeldliste[4])
        self.datenfeldliste[5] = re.sub("[^0-9]", "", self.datenfeldliste[5])