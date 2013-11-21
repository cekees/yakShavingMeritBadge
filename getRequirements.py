import urllib2
import string
from bs4 import BeautifulSoup

name = "Camping"

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
infile = opener.open('http://meritbadge.org/wiki/index.php?title=%s&printable=yes' % (name,))
page = infile.read()
soup= BeautifulSoup(page)
req_outline = soup.find("ol")
i=1
letters = string.ascii_lowercase
for req_i in req_outline.children:
    print i
    import pdb
    #pdb.set_trace()
    #req_a = req_i.children
    #print req_a
    #print len(req_a)
    if len(req_i.contents) > 1:
        a = 0
        for req_a in req_i.children:
            print letters[a]
            a+=1
    i+=1
