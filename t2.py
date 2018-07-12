import bs4
import jinja2
import codecs
from collections import defaultdict

templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(loader=templateLoader)


def visitPart(root):
    parts = root.findAll("Part")
    if parts:
        for x in parts:
            refined_tree["root"].append(x)
            x.html_id = x["Num"]
            x.title = x.find("PartTitle").text
            x.parent_id = "root"
            visitChapter(x)
    else:
        root.html_id = "root"
        visitChapter(root)


def visitChapter(tree):
    for x in tree.findAll("Chapter"):
        refined_tree[tree.html_id].append(x)
        chapter_id = x["Num"]
        if tree.html_id == "root":
            # it's dummy container for laws without parts
            x.html_id = chapter_id
        else:
            x.html_id = "{}.{}".format(tree.html_id, chapter_id)
        x.title = x.find("ChapterTitle").text
        x.parent_id = tree.html_id
        x.parent_group = tree
        visitSection(x)


def visitSection(tree):
    for x in tree.findAll("Section"):
        refined_tree[tree.html_id].append(x)
        section_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, section_id)
        x.title = x.find("SectionTitle").text
        x.parent_id = tree.html_id
        x.parent_group = tree
        visitSubsection(x)


def visitSubsection(tree):
    for x in tree.findAll("Subsection"):
        refined_tree[tree.html_id].append(x)
        subsection_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, subsection_id)
        x.title = x.find("SubsectionTitle").text
        x.parent_id = tree.html_id
        x.parent_group = tree
        visitDivision(x)


def visitDivision(tree):
    for x in tree.findAll("Division"):
        refined_tree[tree.html_id].append(x)
        division_id = x["Num"]
        x.html_id = "{}.{}".format(tree.html_id, division_id)
        x.title = x.find("DivisionTitle").text
        x.parent_id = tree.html_id
        x.parent_group = tree


header_template = templateEnv.get_template("m_header.html")
def render_header(container):
    return header_template.render(
        container=container,
        siblings=refined_tree[container.parent_id],
        children=refined_tree[container.html_id])


article_template = templateEnv.get_template("m_article.html")
def render_articles(group):
    articles = group.findAll("Article")
    address = [group]
    x = group
    while x.parent_group:
        x = x.parent_group
        if x.html_id == "root":
            # it's dummy container for laws without parts
            break
        address = [x] + address

    for a in articles:
        try:
            a.caption = a.find("ArticleCaption").text
        except:
            pass
        a.title = a.find("ArticleTitle").text
        a.html_id = a["Num"]
        paragraphs = a.findAll("Paragraph")
        for p in paragraphs:
            p.paragraph_id = p["Num"]
            p.html_id = "{}.{}".format(a.html_id, p.paragraph_id)
            p.sentences = p.find("ParagraphSentence").findAll("Sentence")
            p.items = p.findAll("Item")
            for x in p.items:
                x.html_id = "{}.{}".format(p.html_id, x["Num"])
        buf.append(article_template.render(article=a, paragraphs=paragraphs, address=address))


def render(item):
    buf.append(render_header(item))
    children = refined_tree[item.html_id]
    if children:
        for x in children:
            render(x)
    else:
        render_articles(item)



def convert_one(target_file):
    global refined_tree, buf
    tree = bs4.BeautifulSoup(open(target_file), "xml")
    refined_tree = defaultdict(list)
    visitPart(tree.MainProvision)  # updates refined_tree

    buf = []
    for x in refined_tree["root"]:
        render(x)  # updates buf

    law_title = tree.find("LawTitle").text

    output_file = target_file.replace("xml", "html")
    base_template = templateEnv.get_template("base.html")
    fo = codecs.open(output_file, "w", encoding="utf-8")
    fo.write(base_template.render(
        law_title=law_title,
        layer1=refined_tree["root"],
        main="\n".join(buf)))
    fo.close()


convert_one("minpo.xml")

def convert_all():
    import glob
    for x in glob.glob("*.xml"):
        print(x)
        convert_one(x)

