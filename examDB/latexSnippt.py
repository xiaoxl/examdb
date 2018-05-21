from pylatex.base_classes import Environment, Command, Container
from pylatex.base_classes.command import CommandBase
from pylatex.utils import NoEscape

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


# class LatexSnipptOutput():
#     @classmethod
#     def dumps_question(cls,json_data):
#         # json_data should have "question" and "solutions"
#         q=LatexSnippt()
#         q.append(Command('question'))
#         q.append(NoEscape(json_data["question"]))
#         for sol in json_data["solutions"]:
#             with q.create(EnvSolutions()):
#                 q.append(NoEscape(sol))
#         return q.dumps()
#
#     @classmethod
#     def dumps_questions(cls,json_list):
#         q=LatexSnippt()
#         with q.create(EnvQuestions()):
#             for question in json_list:
#                 q.append(Command('question'))
#                 q.append(NoEscape(question["question"]))
#                 for sol in question["solutions"]:
#                     with q.create(EnvSolutions()):
#                         q.append(NoEscape(sol))
#         return q.dumps()