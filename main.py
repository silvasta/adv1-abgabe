import re

from utils.util import Datensatz, IfcSlab, IfcRelDefinesbyProperties


def task_1b(entities):
    result = {}
    for entity in entities:
        if entity.ifcEntity in result:
            result[entity.ifcEntity] += 1
        else:
            result[entity.ifcEntity] = 1
    for entity in result:
        print("Insgesamt {} Datensätze für Entitätstyp: {}".format(result[entity],entity))

def task_2a(ifcSlabs):
    hauptdecken = set()
    for count, slab in enumerate(ifcSlabs):
        print("Teil-Decke Nummer {} hat den Namen {} und ist von Typ {}".format(count+1, slab.datenfeldliste[2], slab.datenfeldliste[-1]))
        hauptdecken.add(slab.datenfeldliste[2])
    print("Es gibt insgesamt {} Decken mit {} Teildecken".format(len(hauptdecken),count+1))

def task_2b():
    ifcPropRels = get_entity_list(ifcEntities, "IFCRELDEFINESBYPROPERTIES")
    ifcPropSets = get_entity_list(ifcEntities, "IFCPROPERTYSET")
    ifcPropValues = get_entity_list(ifcEntities, "IFCPROPERTYSINGLEVALUE")

    for propRel in ifcPropRels:
        for slab in ifcSlabs:
            verweis_slab = propRel.datenfeldliste[4]
            if verweis_slab == slab.datensatzId:
                print()
                print("Decke mit IfcEntitäty #{} hat folgende Properties:".format(slab.datensatzId))
                print(propRel)
                for propSet in ifcPropSets:
                    verweis_propset = propRel.datenfeldliste[5]
                    if verweis_propset == propSet.datensatzId:
                        print(propSet)
                        for verweis_value in propSet.datenfeldliste[4]:
                            for property in ifcPropValues:
                                if verweis_value == property.datensatzId:
                                    print(property)



# Gibt eine Liste zurück mit "Datensatz"-Objekten von allen IFC Entitäten
def import_ifc(path):
    ifcFile = open(path)
    entities = []
    for line in ifcFile.readlines():
        entity = Datensatz(line)
        entities.append(entity)
    return entities

# Gibt eine Liste zurück mit "Datensatz"-Objekten oder erweiterten Klassen von einer IFC Entität
def get_entity_list(entities, entity_name):
    entity_List = []
    for entity in entities:
        if entity.ifcEntity == entity_name:
            if entity_name == "IFCSLAB":
                slab = IfcSlab(entity.input)
                entity_List.append(slab)
            if entity_name == "IFCRELDEFINESBYPROPERTIES":
                rel = IfcRelDefinesbyProperties(entity.input)
                entity_List.append(rel)
            else:
                entity.parse_datenfeldliste()
                entity_List.append(entity) 
    return entity_List



if __name__ == '__main__':
    ifcEntities = import_ifc("Architekturmodell_angepasst.ifc")
    # task_1b(ifcEntities)
    ifcSlabs = get_entity_list(ifcEntities, "IFCSLAB")
    # task_2a(ifcSlabs)

    task_2b()