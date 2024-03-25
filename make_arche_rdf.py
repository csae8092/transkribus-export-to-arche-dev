import glob
import os
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader
from rdflib import Namespace, URIRef, RDF, Graph, Literal, XSD


g = Graph().parse("arche_seed_files/arche_constants.ttl")
g_repo_objects = Graph().parse("arche_seed_files/repo_objects_constants.ttl")
TOP_COL_URI = URIRef("https://id.acdh.oeaw.ac.at/my-transkribus-play")

ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
COLS = [ACDH["TopCollection"], ACDH["Collection"], ACDH["Resource"]]
COL_URIS = set()


files = glob.glob("exports/*/*/*/mets.xml")
for x in tqdm(files):
    heads, _ = os.path.split(x)
    # document collection
    cur_col_id = x.split("/")[2]
    cur_col_slug = x.split("/")[3]
    cur_col_uri = URIRef(f"{TOP_COL_URI}/{cur_col_id}/{cur_col_slug}")
    cur_col_title = cur_col_id.replace("-", " ").replace("_", " ")
    g.add((cur_col_uri, RDF.type, ACDH["Collection"]))
    g.add((cur_col_uri, ACDH["isPartOf"], TOP_COL_URI))

    # mets file
    mets = URIRef(f"{cur_col_uri}/mets.xml")
    g.add((mets, RDF.type, ACDH["Resource"]))
    g.add((mets, ACDH["isPartOf"], cur_col_uri))
    g.add((mets, ACDH["hasTitle"], Literal("mets.xml", lang="und")))
    g.add(
        (
            mets,
            ACDH["hasCategory"],
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/model"),
        )
    )

    # parse mets file to extract image-uris and document title
    doc = TeiReader(x)
    cur_col_title = doc.tree.xpath(".//title/text()")[0]
    g.add((cur_col_uri, ACDH["hasTitle"], Literal(cur_col_title, lang="und")))
    # page folder
    page_folder_uri = URIRef(f"{cur_col_uri}/page")
    g.add((page_folder_uri, RDF.type, ACDH["Collection"]))
    g.add((page_folder_uri, ACDH["isPartOf"], cur_col_uri))
    g.add((page_folder_uri, ACDH["hasTitle"], Literal("page files", lang="und")))

    # page files
    page_files = glob.glob(f"{heads}/page/*.xml")
    for y in page_files:
        _, tail = os.path.split(y)
        page_file_uri = URIRef(f"{page_folder_uri}/{tail}")
        g.add((page_file_uri, RDF.type, ACDH["Resource"]))
        g.add((page_file_uri, ACDH["isPartOf"], page_folder_uri))
        g.add((page_file_uri, ACDH["hasTitle"], Literal(tail, lang="und")))
        g.add(
            (
                page_file_uri,
                ACDH["hasCategory"],
                URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/model"),
            )
        )


for x in COLS:
    for s in g.subjects(None, x):
        COL_URIS.add(s)

for x in COL_URIS:
    for p, o in g_repo_objects.predicate_objects():
        g.add((x, p, o))
g.serialize("arche.ttl")
