import simplejson
import os
import cgi
import types
import numpy


class HTMLOutput:

    def __init__(self):
        self.pages = {}
        self.pageorder = []

    def encode_special(self, obj):
        if isinstance(obj, types.GeneratorType):
            return list(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        raise TypeError("%r is not JSON serializable" % type(obj))

    def addstring(self, title, content):
        if title not in self.pages:
            self.pages[title] = ""
        self.pages[title] += cgi.escape(content) + "\n"
        if title not in self.pageorder:
            self.pageorder.append(title)

    def adddata(self, title, content):
        if title not in self.pages:
            self.pages[title] = ""
        self.pages[title] += cgi.escape(simplejson.dumps(content, default=self.encode_special, skipkeys=True, sort_keys=True, indent=4))
        if title not in self.pageorder:
            self.pageorder.append(title)

    def render(self):
        tabs = []
        pages = []
        path = os.path.dirname(os.path.abspath(__file__))

        for title in self.pageorder:
            tabs.append("<div class=\"tab\">" + title + "</div>")
            pages.append("<div class=\"page\" name=\"" + title + "\">" + self.pages[title] + "</div>")

        f = open(path + '/page.template.html', 'r')
        template = f.read()
        f.close()

        template = template.replace('{{TABS}}', ''.join(tabs))
        template = template.replace('{{PAGES}}', ''.join(pages))

        runcounter = self.getandincrementruncounter()

        if not os.path.isdir(path + '/output'):
            os.makedirs(path + '/output')

        outputfile = path + '/output/output.' + str(runcounter) + '.html'
        f = open(outputfile, 'w')
        f.write(template)
        f.close()

        return outputfile

    def getandincrementruncounter(self):
        path = os.path.dirname(os.path.abspath(__file__))

        if not os.path.isfile(path + '/runcounter.txt'):
            rc = open(path + '/runcounter.txt', 'w')
            rc.write("0")
            rc.close()

        rc = open(path + '/runcounter.txt', 'r+')
        runcounter = int(rc.read())
        runcounter += 1
        rc.seek(0)
        rc.write(str(runcounter))
        rc.close()

        return runcounter
