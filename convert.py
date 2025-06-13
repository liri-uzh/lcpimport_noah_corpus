import io
import os

from lcpcli.builder import Corpus
from lxml import etree
from shutil import rmtree

CORPORA = {
    "blick.xml": {
        "name": "Blick am Abig",
        "description": "Newspaper articles from “Blick am Abig”, Version Zurich, Nr. 97, 28. Mai 2013",
        "date": "2013",
    },
    "blogs.xml": {
        "name": "BlogSpot",
        "description": "BlogSpot blogs",
        "date": "31.1.2014",
    },
    "schobinger.xml": {
        "name": "Viktor Schobinger novels",
        "description": "Extracts of criminal novels by Viktor Schobinger",
        "date": "2014",
    },
    "swatch.xml": {
        "name": " SWATCH annual report",
        "description": "SWATCH annual report",
        "date": "2012",
    },
    "wiki.xml": {
        "name": "Alemannic Wikipedia",
        "description": "Articles from the Alemannic Wikipedia",
        "date": "10.4.2012",
    },
}


def run(fn: str, name: str, description: str, date: str):
    dirname, _ = os.path.splitext(os.path.basename(fn))
    odir = os.path.join("output", dirname)
    if os.path.exists(odir):
        rmtree(odir)
    os.makedirs(odir)

    c = Corpus(
        name,
        document="Article",
        segment="Sentence",
        token="Word",
        author="Nora Hollenstein and Noëmi Aepli and Simon Clematide",
        description=description,
        date=date,
        url="https://noe-eva.github.io/NOAH-Corpus/",
    )

    tree = etree.parse(io.BytesIO(open(fn, "rb").read()))
    root = tree.getroot()

    for na, article in enumerate(root.findall("article")):
        title = article.get("title", "")
        number_a = article.get("n", str(na))
        a = c.Article(title=title, num=number_a)
        for ns, segment in enumerate(article.findall("s")):
            number_s = segment.get("n", f"{number_a}-{ns}")
            s = a.Sentence(num=number_s)
            for nw, word in enumerate(segment.findall("w")):
                number_w = word.get("n", f"{number_a}-{number_s}-{nw}")
                pos = word.get("pos", "")
                verified = word.get("verified", "")
                form = word.text or ""
                s.Word(form, num=number_w, pos=pos, verified=verified)
        a.make()

    c.make(odir)


for fn, details in CORPORA.items():
    run(fn, **details)
