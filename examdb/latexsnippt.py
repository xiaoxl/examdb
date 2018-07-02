from pylatex.base_classes import Environment, Command, Container
from pylatex.base_classes.command import CommandBase
from pylatex.utils import NoEscape

'''
This is a file contains several class to generate Latex snippts wich emphasis on examdb usage.

LatexSnippt is used as Document class, without any packages and head files. Others are just custom environments and commands.
'''

class EnvParts(Environment):
    _latex_name='parts'

class ComPart(CommandBase):
    _latex_name = 'part'

class EnvQuestions(Environment):
    _latex_name='questions'

class EnvSolutions(Environment):
    _latex_name='solution'

class ComQuestion(CommandBase):
    _latex_name='question'

class LatexSnippt(Container):
    omit_if_empty = False

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def dumps(self):

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        return content
