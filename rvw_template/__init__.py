from abc import ABC, abstractmethod
import html
from .rvw_general_template import *


class HO(ABC):
    def __init__(self, objs=[]):
        self.objs = objs
        self.scripts = []

    def addScript(self, script):
        self.scripts.append(script)

    def addHO(self, obj):
        self.objs.append(obj.toHTML())
        for scr in obj.scripts:
            self.addScript(scr)

    @abstractmethod
    def toHTML(self):
        pass

class Div(HO):
    def __init__(self, html_class, objs=[]):
        super(Div, self).__init__(objs)
        self.html_class = html_class

    def toHTML(self):
        return '''
        <div class="{}">
        {}
        </div>
        '''.format(self.html_class,'\n\t'.join(self.objs))

class Card(HO):
    def __init__(self, html_class, objs = [], header = None, footer = None):
        super(Card, self).__init__(objs)
        self.html_class = html_class
        self.header = header
        self.footer = footer

    def toHTML(self):
        htheader = ""
        htfooter = ""
        if self.header:
            htheader = '<div class="card-header mt-2">{}</div>'.format(self.header)
        if self.footer:
            htfooter = '<div class="card-footer text-muted mb-2">{}</div>'.format(self.footer)
        return '''
        <div class="card {}">
        {}
        {}
        {}
        </div>
        '''.format(self.html_class, htheader ,'\n\t'.join(self.objs), htfooter)

class SimpleCard(Card):
    def __init__(self, objs = []):
        super(SimpleCard, self).__init__("text-center", objs)

class Form(HO):
    def __init__(self, id, objs=[]):
        super(Form, self).__init__(objs)
        self.id = id

    def toHTML(self):
        return '''
        <form class="form" id="{}">
        {}
        </form>
        '''.format(self.id,'\n\t'.join(self.objs))