import json
import os


class HTMLOutput:

    def __init__(self):
        self.pages = {}

    def addstring(self, title, content):
        self.pages[title] = content

    def adddata(self, title, content):
        self.pages[title] = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))

    def render(self):
        tabs = []
        pages = []
        path = os.path.dirname(os.path.abspath(__file__))

        for title in self.pages:
            tabs.append("<div class=\"tab\">" + title + "</div>")
            pages.append("<div class=\"page\" name=\"" + title + "\">" + self.pages[title] + "</div>")

        f = open(path + '/page.template.html', 'r')
        template = f.read()
        f.close()

        template = template.replace('{{TABS}}', ''.join(tabs))
        template = template.replace('{{PAGES}}', ''.join(pages))

        f = open(path + '/output.html', 'w')
        f.write(template)
        f.close()

        return path + '/output.html'
