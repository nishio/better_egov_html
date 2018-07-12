import bs4
import jinja2
import codecs
from collections import defaultdict

templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "base.html"
#template = templateEnv.get_template("base.html")
#outputText = template.render()


tree = bs4.BeautifulSoup(open("minpo.xml"), "xml")
refined_tree = defaultdict(list)

def visitPart(tree):
    for x in tree.findAll("Part"):
        refined_tree["root"].append(x)
        x.html_id = x["Num"]
        x.title = x.find("PartTitle").text
        x.parent_id = "root"
        visitChapter(x)

def visitChapter(tree):
    for x in tree.findAll("Chapter"):
        refined_tree[tree.html_id].append(x)
        chapter_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, chapter_id)
        x.title = x.find("ChapterTitle").text
        x.parent_id = tree.html_id
        visitSection(x)

def visitSection(tree):
    for x in tree.findAll("Section"):
        refined_tree[tree.html_id].append(x)
        section_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, section_id)
        x.title = x.find("SectionTitle").text
        x.parent_id = tree.html_id
        visitSubsection(x)

def visitSubsection(tree):
    for x in tree.findAll("Subsection"):
        refined_tree[tree.html_id].append(x)
        subsection_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, subsection_id)
        x.title = x.find("SubsectionTitle").text
        x.parent_id = tree.html_id
        visitDivision(x)

def visitDivision(tree):
    for x in tree.findAll("Division"):
        refined_tree[tree.html_id].append(x)
        division_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, division_id)
        x.title = x.find("DivisionTitle").text
        x.parent_id = tree.html_id

visitPart(tree.MainProvision)


def foo(article):
    print(article.ArticleCaption.text)
    print(article.ArticleTitle.text)
    for p in article.findAll("Paragraph"):
        print("p{}".format(p["Num"]))
        for s in p.findAll("Sentence"):
            s_id = s.get("Num", "0")
            print("s{} {}".format(s_id, s.text))

#foo(tree.find("Article", Num="556"))

header_template = templateEnv.get_template("m_header.html")
def render_header(item):
    return header_template.render(
        item=item,
        siblings=refined_tree[item.parent_id],
        children=refined_tree[item.html_id])

buf = []
#render_header(refined_tree["3"][0])
def render(item):
    buf.append(render_header(item))
    for x in refined_tree[item.html_id]:
        render(x)

for x in refined_tree["root"]:
    render(x)

base_template = templateEnv.get_template("base.html")
fo = codecs.open("minpo.html", "w", encoding="utf-8")
fo.write(base_template.render(main="\n".join(buf)))
fo.close()
