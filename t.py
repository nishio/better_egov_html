# -*- encoding: utf-8 -*-

import csv, codecs
reader = csv.reader(codecs.open("minpo.csv", encoding="sjis"))
# hen, show, setu, kan, moku
section_id = [0] * 5
section_name = [""] * 5

rows = list(reader)
law_name = rows[0][0]
header = rows[1]

fo = codecs.open("minpo.html", "w", encoding="utf-8")
fo.write("""<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script
       src="https://code.jquery.com/jquery-3.3.1.min.js"
       integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
       crossorigin="anonymous"></script>
    <script src="main.js"></script>
<body>
<div style="width: 100%; word-break: break-all">
<span id='x1'>[x1]</span> <span id='x2'>[x2]</span>
""")
section_suffix = ["編", "章", "節", "款", "目"]
for row in rows[2:]:

    for i in range(5):
        if row[i * 2]:
            section_id[i] = row[i * 2]
            section_name[i] = row[i * 2 + 1]
            for j in range(i + 1, 5):
                section_id[j] = 0
            html_id = "s" + ".".join(section_id[:i+1])
            fo.write("<h3 id='{}'><a href='#{}'>{}{} {}</a></h3>\n".format(html_id, html_id, section_id[i], section_suffix[i], section_name[i]))

    address = ""
    for i in range(5):
        if section_id[i]:
            html_id = "s" + ".".join(section_id[:i+1])
            address += "<a href='#{}'>{}{} {}</a> ".format(html_id, section_id[i], section_suffix[i], section_name[i])

    if row[10]:
        jou = row[10]
        jou_title = row[11]

    kou = row[12]
    gou = row[13]
    html_id = jou

    jou_address = "<a href='#{}'>{}条</a>".format(jou, jou, jou)

    if kou:
        html_id = "{}.{}".format(jou, kou)
        jou_address += " <a id='{}' href='#{}'>{}項</a>".format(html_id, html_id, kou)
    if gou:
        html_id = "{}.{}.{}".format(jou, kou, gou)
        jou_address += " <a id='{}' href='#{}'>{}号</a>".format(html_id, html_id, gou)

    body = row[14]
    #print("{address}\n{jou_address}\n{body}".format(**globals()))
    fo.write("""
    <div style='border-style: solid; padding: 0.5em;' id='{jou}'>
<p style='margin: 0'>{address}<br>
{jou_title}</p>
<p><strong>{jou_address}</strong> <span class='body'>{body}</span> <span class='copy'>[copy]</span></p>
</div>\n
""".format(**globals()))

fo.close()



