from pylatex import Document, Section, Subsection, Package, Command, Math,MiniPage
from pylatex.lists import List,Itemize,Enumerate
from pylatex.utils import italic, NoEscape
from pylatex.base_classes.command import Arguments,CommandBase
# from pylatex.base_classes.latex_object import LatexObject
from pylatex.base_classes.containers import *
import json
from pprint import pprint
import random


class Env_Parts(Environment):
    _latex_name='parts'

class Com_Part(CommandBase):
    _latex_name = 'part'

class Env_Questions(Environment):
    _latex_name='questions'

class Com_Question(CommandBase):
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
    # packages and some basic settings
    doc.packages.append(Package('amssymb, amsfonts, latexsym, verbatim, xspace, setspace,tikz,multicol,amsmath,multirow'))
    doc.packages.append(Package('geometry','margin=1in'))

    doc.packages.append(Command('usetikzlibrary','plotmarks'))
    doc.packages.append(Command('singlespacing'))
    doc.packages.append(Command('parindent 0ex'))

    # course configurations
    data_class=r'Math 9C: Calculus'
    data_term=r'2018W'
    data_examnum=r'Final'
    data_date=r'03/23/2018'
    data_timelimit=r'180min'

    # grade table setting
    gradetablesetting='v'
    # gradetablesetting='v][page'

    doc.packages.append(Command('newcommand',Arguments(Command('class'),NoEscape(data_class))))
    doc.packages.append(Command('newcommand',Arguments(Command('term'),NoEscape(data_term))))
    doc.packages.append(Command('newcommand',Arguments(Command('examnum'),NoEscape(data_examnum))))
    doc.packages.append(Command('newcommand',Arguments(Command('examdate'),NoEscape(data_date))))
    doc.packages.append(Command('newcommand',Arguments(Command('timelimit'),NoEscape(data_timelimit))))

    # some formation setting
    doc.append(Command('pagestyle','head'))
    doc.append(Command('firstpageheader',Arguments('', '', '')))

    # draw header, from head.head file
    doc.append(Command('runningheader',Arguments(Command('class'),NoEscape(r'\examnum\ - Page \thepage\ of \numpages'))))
    doc.append(Command('runningheadrule'))

    with doc.create(LatexFulsh()) as fulsh:
        with fulsh.create(LatexTabular(arguments=NoEscape(r'p{2.8in} r l'))) as tabs:
            with open('edb_head/head.head','r') as file:
                header=file.read().split('<__|__>')
                tabs.append(NoEscape(header[0]))
        fulsh.append(NoEscape(r'\\'))
    doc.append(Command('rule',options='1ex',arguments=Arguments(Command('textwidth'),'.1pt')))

    doc.append(Command('newcommand',Arguments(Command('boxwidth'),'0.8cm')))

    # draw statemnts, from book_note_cal_work.head, instructions for students
    with open('edb_head/book_note_cal_work.head','r') as file:
        con=file.read()
        content=con.split('<__|__>')

    doc.append(NoEscape(content[0]))
    with doc.create(MiniPage(width='3.7in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        with minipage.create(Itemize()) as items:
            for itemcont in content[1:]:
                items.add_item(NoEscape(itemcont))

        minipage.append(NoEscape(r'Do not write in the table to the right.'))

    # draw the score table
    doc.append(Command('hfill'))
    with doc.create(MiniPage(width='2.3in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        minipage.append(Command('gradetablestretch','2'))
        minipage.append(Command('vqword','Problem'))
        minipage.append(Command('addpoints'))
        minipage.append(Command('gradetable',options=NoEscape(gradetablesetting)))

    doc.append(Command('newpage'))
    doc.append(Command('addpoints'))



    with open('problemdb.json','r') as data_file:
        content=json.loads(data_file.read())


        k=0

        question='\n'.join(content[k]["question"])
        parts=content[k]["part"]
        number_of_parts=len(parts)
        if number_of_parts>1:
            pass
        solution='\n'.join(content[k]['solution'][0])
        varchange=content[k]['varchange']
        tag=content[k]['tag']
        for i in range(len(varchange)):
            exec(varchange[i])
            exec('temp=var'+str(i))
            question=question.replace('_var'+str(i)+'_',str(temp))
            solution=solution.replace('_var'+str(i)+'_',str(temp))




    with doc.create(Env_Questions()) as question:
        question.append(Com_Question())
        with question.create(Env_Parts()) as inside:
            inside.append(Com_Part(options=3))
            inside.append(NoEscape(question))
            inside.append(NoEscape(solution))
            inside.append(Com_Part(options=3))
            inside.append(NoEscape(r'dfasfsafsafsadfasd'))

            inside.append(Com_Part(options=3))
            inside.append(NoEscape(r'dfasfsafsafsadfasd'))

            inside.append(Command('newpage'))

    doc.generate_tex()
    # doc.generate_pdf(clean_tex=False)
