from pylatex import Document, Package, Command, MiniPage
from pylatex.lists import List,Itemize,Enumerate
from pylatex.utils import italic, NoEscape
from pylatex.base_classes.command import Arguments,CommandBase
from pylatex.base_classes.containers import *
from examDB.latexSnippt import LatexSnippt
from pylatex.utils import *
from pylatex import *

class LatexFulsh(Environment):
    _latex_name='flushright'

class LatexTabular(Environment):
    _latex_name='tabular'


class ExamCls(LatexSnippt):

    __class__=r'Math 9C: Calculus'
    __term__=r'2018W'
    __examnum__=r'Final'
    __date__=r'03/23/2018'
    __timelimit__=r'180min'

    # preamble=[]
    # def set_class(self,var):
    #     __class__=var
    #
    # def set_term(self,term):
    #     __term__=term
    #
    # def set_examnum(self,var):
    #     __examnum__=var
    #
    # def set_date(self,var):
    #     __date__=var
    #
    # def set_timelimit(self,var):
    #     __timelimit__=var

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fillFilehead(self):
        self.preamble.append(Command('usetikzlibrary','plotmarks'))
        self.preamble.append(Command('singlespacing'))
        self.preamble.append(Command('parindent 0ex'))

    # course configurations
        self.preamble.append(Command('newcommand',Arguments(Command('class'),NoEscape(self.__class__))))
        self.preamble.append(Command('newcommand',Arguments(Command('term'),NoEscape(self.__term__))))
        self.preamble.append(Command('newcommand',Arguments(Command('examnum'),NoEscape(self.__examnum__))))
        self.preamble.append(Command('newcommand',Arguments(Command('examdate'),NoEscape(self.__date__))))
        self.preamble.append(Command('newcommand',Arguments(Command('timelimit'),NoEscape(self.__timelimit__))))

    # document starts
    # some formation setting
        self.append(Command('pagestyle','head'))
        self.append(Command('firstpageheader',Arguments('', '', '')))

    # draw header, from head.head file
        self.append(Command('runningheader',Arguments(Command('class'),NoEscape(r'\examnum\ - Page \thepage\ of \numpages'))))
        self.append(Command('runningheadrule'))

        with self.create(LatexFulsh()) as fulsh:
            with fulsh.create(LatexTabular(arguments=NoEscape(r'p{2.8in} r l'))) as tabs:
                with open('edb_setting/header.cfg','r') as file:
                    header=file.read().split('<__|__>')
                    tabs.append(NoEscape(header[0]))
            fulsh.append(NoEscape(r'\\'))

        self.append(Command('rule',options='1ex',arguments=Arguments(Command('textwidth'),'.1pt')))
        self.append(Command('newcommand',Arguments(Command('boxwidth'),'0.8cm')))

    # draw statemnts, from coverpage.cfg, instructions for students
        with open('edb_setting/coverpage.cfg','r') as file:
            con=file.read()
            content=con.split('<__|__>')

        self.append(NoEscape(content[0]))
        with self.create(MiniPage(width='3.7in',pos='t')) as minipage:
            minipage.append(Command('vspace','0pt'))
            with minipage.create(Itemize()) as items:
                for itemcont in content[1:]:
                    items.add_item(NoEscape(itemcont))

            minipage.append(NoEscape(r'Do not write in the table to the right.'))

    # draw the score table
        self.append(Command('hfill'))
        with self.create(MiniPage(width='2.3in',pos='t')) as minipage:
            minipage.append(Command('vspace','0pt'))
            minipage.append(Command('gradetablestretch','2'))
            minipage.append(Command('vqword','Problem'))
            minipage.append(Command('addpoints'))
            # grade table setting
            gradetablesetting='v'
            # gradetablesetting='v][page'
            minipage.append(Command('gradetable',options=NoEscape(gradetablesetting)))

        self.append(Command('newpage'))

    def dumps(self):

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        return content