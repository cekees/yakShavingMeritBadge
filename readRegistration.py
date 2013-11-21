import urllib2
import string
from bs4 import BeautifulSoup
letters = string.ascii_lowercase
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def getRequirements(name):
    requirementsList=[]
    infile = opener.open('http://meritbadge.org/wiki/index.php?title=%s&printable=yes' % (name,))
    page = infile.read()
    infile.close()
    soup= BeautifulSoup(page)
    req_outline = soup.find("ol")
    i=1
    for req_i in req_outline.children:
        if str(req_i).isspace():
            continue
        else:
            if len(req_i.contents) > 1 and req_i.contents[1].name != "a":
                a = 0
                for req_a in req_i.children:
                    if str(req_a).isspace():
                        continue
                    elif req_a.name == "a":
                        continue
                    else:
                        requirementsList.append(`i`+letters[a])
                        a+=1
            else:
                requirementsList.append(`i`)
            i+=1
    return requirementsList

import csv
import re
meritBadgeClasses = {}
meritBadgeRequirements = {}
with open ("registration.csv","rb") as csvfile:
    csvfile.next()
    scoutreader = csv.reader(csvfile, delimiter='\t')
    for row in scoutreader:
        row[3]
        meritBadgeClass = row[3]
        scout = (row[0],row[1],re.sub(r'\([^)]*\)','',row[2]))
        meritBadge = meritBadgeClass[:meritBadgeClass.find('Nov')].lstrip().rstrip().replace("Auto","Automotive").replace("(Mountain Biking Option)","").replace("Prepareness","Preparedness").replace("MGT","Management").replace("Veterninary","Veterinary").replace(" ","_")
        section = meritBadgeClass[meritBadgeClass.find('Nov'):]
        if meritBadge[:6] != 'Winter':
            if not meritBadgeRequirements.has_key(meritBadge):
                print "getting requirements for ",meritBadge
                meritBadgeRequirements[meritBadge] = getRequirements(meritBadge)
                print meritBadgeRequirements[meritBadge]
            if section.count("Nov 23"):
                if section.count("AM"):
                    key = (meritBadge,"Sat/Sun AM")
                    if meritBadgeClasses.has_key(key):
                        meritBadgeClasses[key].append(scout)
                    else:
                        meritBadgeClasses[key] = [scout]
                elif section.count("PM"):
                    key = (meritBadge,"Sat/Sun PM")
                    if meritBadgeClasses.has_key(key):
                        meritBadgeClasses[key].append(scout)
                    else:
                        meritBadgeClasses[key] = [scout]
            elif section.count("Nov 25"):
                if section.count("AM"):
                    key = (meritBadge,"Mon/Tue AM")
                    if meritBadgeClasses.has_key(key):
                        meritBadgeClasses[key].append(scout)
                    else:
                        meritBadgeClasses[key] = [scout]
                elif section.count("PM"):
                    key = (meritBadge,"Mon/Tue PM")
                    if meritBadgeClasses.has_key(key):
                        meritBadgeClasses[key].append(scout)
                    else:
                        meritBadgeClasses[key] = [scout]

latexfile = open("meritBadgeCharts.tex",'w')
docheader = r"""
\documentclass{report}
\usepackage[landscape,pdftex]{geometry}
\setlength{\oddsidemargin}{-0.5in}   
\setlength{\evensidemargin}{-0.5in}   
\setlength{\topmargin}{-0.25in}   
\setlength{\headheight}{0.0in}   
\setlength{\headsep}{0.0in}   
\setlength{\topskip}{0in}   
\setlength{\footskip}{0.15in}   
\setlength{\textwidth}{6.5in}   
\setlength{\textheight}{9in}   
\begin{document}
"""
latexfile.write(docheader)

for k,v in meritBadgeClasses.iteritems():
    latexfile.write("{\\bf %s~~~~~~~~~%s}" % (k[0].replace("_"," "),k[1]))
    requirementsList = meritBadgeRequirements[k[0]]
    fontsize="large"
    nr = len(requirementsList)
    if nr > 18:
        fontsize="tiny"
    elif nr > 16:
        fontsize="scriptsize"
    elif nr > 14:
        fontsize="footnotesize"
    elif nr > 12:
        fontsize="small"
    else:
        fontsize="normalsize"
    colspec = "l|l|l|c|c"+len(requirementsList)*"|c"
    cols = "First & Last & Troop & D1 & D2"
    newcols=""
    for r in requirementsList:
        cols+= "&"+r
        newcols+=  " & "
    cols+="\\\ \n"
    tableheader = r"""

\vspace{0.5in}
\begin{"""+fontsize+r"""}
\begin{tabular}{"""+colspec+"""}
"""+cols+"""
\hline
"""
    latexfile.write(tableheader)
    for scout in v:
        latexfile.write("%s & %s & %s & & %s \\\ \n \hline \n" % (scout[1],scout[0],scout[2].replace("Troop",""),newcols))
    tablefooter = r"""
\end{tabular}
\end{"""+fontsize+r"""}
\newpage
"""
    latexfile.write(tablefooter)

docfooter = r"""\end{document}
"""
latexfile.write(docfooter)
latexfile.close()

latexfile2 = open("bluecards.tex",'w')
docheader = r"""
\documentclass[twocolumn]{report}
\usepackage[pdftex]{geometry}
\setlength{\oddsidemargin}{-0.5in}   
\setlength{\evensidemargin}{-0.5in}   
\setlength{\topmargin}{-0.25in}   
\setlength{\headheight}{0.0in}   
\setlength{\headsep}{0.0in}   
\setlength{\topskip}{0in}   
\setlength{\footskip}{0.15in}   
\setlength{\columnwidth}{3.75in}   
\setlength{\textwidth}{7.5in}   
\setlength{\textheight}{9in}
\setlength{\parindent}{0in}
\begin{document}
"""
latexfile2.write(docheader)

for k,v in meritBadgeClasses.iteritems():
    for scout in v:
        latexfile2.writelines(["\\begin{tabular*}{3.5in}{@{\\extracolsep{\\fill} }|lr|}\n",
                               "\\hline\n",
                               "{\\bf %s } &{\\bf %s} \\\ \n" % (k[0].replace("_"," "),k[1]),
                               "\\hline\n",
                               "%s  %s  & Troop %s \\\ \n" % (scout[1],scout[0],scout[2].replace("Troop","")),
                               "\\hline\n & \\\ \n",
                               "Remaining: & \\\ \n"])
        latexfile2.write(r"""\hline
& \\
Counselor: & \\
\hline
& \\
Signature: & \\
\hline
\end{tabular*}
\\
\\
\\
""")
    latexfile2.writelines([r"\newpage"])

docfooter = r"""\end{document}
"""
latexfile2.write(docfooter)
latexfile2.close()
