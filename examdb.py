from pylatex import Document, Section, Subsection, Package, Command, Math,MiniPage
from pylatex.lists import List,Itemize,Enumerate
from pylatex.utils import italic, NoEscape
from pylatex.base_classes.command import Arguments,CommandBase
from pylatex.base_classes.latex_object import LatexObject
from pylatex.base_classes.containers import *

class QParts(Environment):
    _latex_name='parts'

class QPart(CommandBase):
    _latex_name = 'part'

class Questions(Environment):
    _latex_name='questions'

class LatexQuestion(CommandBase):
    _latex_name='question'

class LatexFulsh(Environment):
    _latex_name='flushright'

class LatexTabular(Environment):
    _latex_name='tabular'

if __name__ == '__main__':
    # Basic document
    doc = Document('examdb',
                   documentclass='exam',
                   document_options='11pt',
                   fontenc=None,
                   inputenc=None,
                   # font_size=None,
                   textcomp=False,
                   lmodern=False,
                   # page_numbers=False
                   )
    doc.packages.append(Package('amssymb, amsfonts, latexsym, verbatim, xspace, setspace,tikz,multicol,amsmath,multirow'))
    doc.packages.append(Package('geometry','margin=1in'))
    doc.packages.append(Command('usetikzlibrary','plotmarks'))

    data_class=r'Math 9C: Calculus'
    data_term=r'2018W'
    data_examnum=r'Final'
    data_date=r'03/23/2018'
    data_timelimit=r'180min'

    doc.packages.append(Command('newcommand',Arguments(Command('class'),NoEscape(data_class))))
    doc.packages.append(Command('newcommand',Arguments(Command('term'),NoEscape(data_term))))
    doc.packages.append(Command('newcommand',Arguments(Command('examnum'),NoEscape(data_examnum))))
    doc.packages.append(Command('newcommand',Arguments(Command('examdate'),NoEscape(data_date))))
    doc.packages.append(Command('newcommand',Arguments(Command('timelimit'),NoEscape(data_timelimit))))
    # \newcommand{\class}{}
    # \newcommand{\term}{Winter 2018}
    # \newcommand{\examnum}{Final}
    # \newcommand{\examdate}{03/23/2018}
    # \newcommand{\timelimit}{180 Minutes}
    #


    doc.packages.append(Command('singlespacing'))
    doc.packages.append(Command('parindent 0ex'))


    doc.append(Command('pagestyle','head'))
    doc.append(Command('firstpageheader',Arguments('', '', '')))


    doc.append(Command('runningheader',Arguments(Command('class'),NoEscape(r'\examnum\ - Page \thepage\ of \numpages'))))
    doc.append(Command('runningheadrule'))

    with doc.create(LatexFulsh()) as fulsh:
        with fulsh.create(LatexTabular(arguments=NoEscape(r'p{2.8in} r l'))) as tabs:
            tabs.append(NoEscape(r'''\textbf{\class} & \textbf{Name (Print):} & \makebox[1.9in]{\hrulefill}\\
    \textbf{\term} &&\\
    \textbf{\examnum} &\textbf{Discussion TA:}&\makebox[1.9in]{\hrulefill}\\
    \textbf{\examdate} &&\\
    \textbf{Time Limit: \timelimit} &\textbf{Discussion time:}&\makebox[1.9in]{\hrulefill}'''))
        fulsh.append(NoEscape(r'\\'))
    doc.append(Command('rule',options='1ex',arguments=Arguments(Command('textwidth'),'.1pt')))




    doc.append(Command('newcommand',Arguments(Command('boxwidth'),'0.8cm')))

    doc.append(NoEscape(r'''
    This exam contains \numpages\ pages (including this cover page) and \numquestions\ problems.  Check to see if any pages are missing.  Enter all requested information on the top of this page, and put your initials on the top of every page, in case the pages become separated.\\
    You may \textbf{NOT} use your books, notes, or any calculator on this exam.\\
    You are required to show your work on each problem on this exam.  The following rules apply:\\
    '''))
    #
    with doc.create(MiniPage(width='3.7in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        with minipage.create(Itemize()) as items:
            items.add_item(NoEscape(r'''\textbf{Organize your work}, in a reasonably neat and coherent way, in
            the space provided. Work scattered all over the page without a clear ordering will
            receive very little credit.'''))
            items.add_item(NoEscape(r'''\textbf{Mysterious or unsupported answers will not receive full
credit}.  A correct answer, unsupported by calculations, explanation,
or algebraic work will receive no credit; an incorrect answer supported
by substantially correct calculations and explanations might still receive
partial credit.
            '''))
            items.add_item(NoEscape(r'If you need more space, use the back of the pages; clearly \textbf{indicate} when you have done this.'))
            items.add_item(NoEscape(r'All problems should be answered in \textbf{exact values}, not decimal approximations (unless instructed explicitly to do so).'))

        minipage.append(NoEscape(r'Do not write in the table to the right.'))

    doc.append(Command('hfill'))
    with doc.create(MiniPage(width='2.3in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        minipage.append(Command('gradetablestretch','2'))
        minipage.append(Command('vqword','Problem'))
        minipage.append(Command('addpoints'))
        minipage.append(Command('gradetable',options='v'))

    doc.append(Command('newpage'))
    doc.append(Command('addpoints'))



    with doc.create(Questions()) as question:
        question.append(LatexQuestion())
        with question.create(QParts()) as inside:
            inside.append(QPart(options=3))
            inside.append(NoEscape(r'dfasfsafsafsadfasd'))

            inside.append(QPart(options=3))
            inside.append(NoEscape(r'dfasfsafsafsadfasd'))

            inside.append(QPart(options=3))
            inside.append(NoEscape(r'dfasfsafsafsadfasd'))

            inside.append(Command('newpage'))

    doc.generate_tex()
    # doc.generate_pdf(clean_tex=False)
