#!/usr/bin/python3
#!/usr/bin/env python3
import locale
import os
import sys
import locale
import os
import sys

import cgi
import os
import json
import sys
import base64 as b64
from chinese import *
from modules import *
print("Content-type: text/html\n\n")
print("")
form = cgi.FieldStorage()
Action = form.getfirst("RequestType")
JSONbuf = {}
jEncode = json.JSONEncoder().encode
bookDir = WEB_ROOT+"cBooks/books/"
SubDivider = Chin["interpunct"]   # symbol to indicate subdivision by category ex 賦-卷一.html
Entry=Creator(FindRegex,rgx='(<div class="biji_block">.*?</div>)(?=\W{0,}<div class="biji_block">|\W{0,}</body>)')

if Action == "ListBooks":
    JSONbuf['booklist'] = shell_exec("ls {0}".format(bookDir)).decode("utf-8").split("\n")[:-1]
    
elif Action == "ListChapters":
    targetBook=form.getfirst("BookName")
    targetBook=b64.urlsafe_b64decode(targetBook).decode("utf-8")
    BookRoot="{0}{1}/".format(bookDir,targetBook).replace(";","")
    chapterFiles = os.listdir(BookRoot)
    JSONbuf['chapterlist'] = [x.replace(BookRoot,"").replace("/",SubDivider).split(".")[0] for x in ChiBookSort(chapterFiles)]
        
    
elif Action == "ListChapters":
    targetBook=form.getfirst("BookName")
    targetBook=b64.urlsafe_b64decode(targetBook).decode("utf-8")
    BookRoot="{0}{1}/".format(bookDir,targetBook).replace(";","")
    try:
        for subDir in os.listdir(BookRoot):
            chapterFiles += [SubDivider.join([subDir,x]) for x in os.listdir(BookRoot+subDir)]
    except NotADirectoryError:
        chapterFiles = os.listdir(BookRoot)

    JSONbuf['chapterlist'] = [x.replace(BookRoot,"").replace("/",SubDivider).split(".")[0] for x in ChiBookSort(chapterFiles)]

elif Action == "SearchContent":
    Book=b64.urlsafe_b64decode(form.getfirst("BookName")).decode('utf-8')
    Chapter=b64.urlsafe_b64decode(form.getfirst("ChapterName")).decode('utf-8')
    Contents=b64.urlsafe_b64decode(form.getfirst("SearchContents")).decode('utf-8')
    Range=b64.urlsafe_b64decode(form.getfirst("SearchRange")).decode('utf-8')
    Comment=Creator(FindRegex,rgx='<span class="zhipi">(.*?)</span>',Remove=True if Range=="zhengwen" else False)
    TargetPath = "^.*?\.html" # default search through everything
    if Chapter != "*":    # specific Chapter -> specific Book
        TargetPath = "{0}/{1}.html".format(Book,Chapter)
    elif Book != "*":     # otherwise all Chapters within specific Book
        TargetPath = ("{0}/".format(Book))+TargetPath
    
    TargetPath = bookDir+TargetPath
    S=Node()
    [d+Entry for d in populate_data(S,TargetPath,Recursive=True)]
    [e+Comment for e in Entry.children]
    TargetData = Comment if Range == "zhushi" else Entry
    JSONbuf.__setitem__("results",[])
    for e in TargetData==Contents:
        e.content = re.sub("({0})".format(Contents),'<span class="match_text">{0}</span>'.format(r"\1"),e.content.decode("utf-8"),0,re.DOTALL|re.MULTILINE)
        parentFile=(-(e<<File))
        cur_book = parentFile.split("/")[-2:]
        cur_book[0] = Chin["open_title_caret"]+cur_book[0]+Chin["close_title_caret"]
        FinalSource = bytes(Chin["interpunct"].join(cur_book).replace(".html",""),encoding="utf-8")
        JSONbuf['results'].append({'source':b64.urlsafe_b64encode(FinalSource).decode("utf-8"),'contents':b64.urlsafe_b64encode(bytes(-e,encoding="utf-8")).decode("utf-8")})
print(jEncode(JSONbuf))
