from pathlib import Path
import json
from rdflib import Graph, Namespace
from rdflib.namespace import PROV, RDF, SDO
AROLE = Namespace("https://data.idnau.org/pid/vocab/idn-role-codes/")
IROLE = Namespace("http://def.isotc211.org/iso19115/-1/2018/CitationAndResponsiblePartyInformation/code/CI_RoleCode/")

g = Graph()
for f in Path("../data").iterdir():
    if f.suffix == ".ttl":
        g.parse(f)

for f in Path("../data/background").iterdir():
    if f.suffix == ".ttl":
        g.parse(f)

# Nodes
nodes = []
for s, o in g.subject_objects(RDF.type):
    i = str(s)
    l = str(g.value(s, SDO.name))
    if o == SDO.Person:
        c = "#D7C29A"
        sh = "triangle"
    elif o == SDO.Organization:
        c = "#F9D1BF"
        sh = "triangle"
    elif o == SDO.Project:
        c = "#C4C0FF"
        sh = "box"
    elif o in [SDO.Article, SDO.Thesis]:
        c = "#FFFFD7"
        sh = "ellipse"

    nodes.append({"id": i, "label": l, "shape": sh, "color": c, "widthConstraint": {"maximum": 250}})


# Edges
edges = []
for s, o in g.subject_objects(SDO.parentOrganization):
    edges.append({"from": str(s), "to": str(o), "label": "parent", "arrows": {"to": {"type": "curve"}}})

for s, o in g.subject_objects(SDO.memberOf):
    edges.append({"from": str(s), "to": str(o), "label": "member of", "arrows": "to", "color": {"color": "green"}})

for s, o in g.subject_objects(SDO.author):
    edges.append({"from": str(o), "to": str(s), "label": "author", "arrows": "to", "color": {"color": "red"}})

for s, bn in g.subject_objects(PROV.qualifiedAssociation):
    r = g.value(bn, PROV.hadRole)
    rl = g.value(r, SDO.name)
    for a in g.objects(bn, PROV.agent):
        edges.append({"from": str(a), "to": str(s), "label": str(rl), "arrows": "to", "color": {"color": "red"}})


open("nodes.json", "w").write(json.dumps(nodes, indent=4))
open("edges.json", "w").write(json.dumps(edges, indent=4))

