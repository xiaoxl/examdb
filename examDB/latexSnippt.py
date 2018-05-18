from pylatex.base_classes import Container

class LatexSnippt(Container):
    omit_if_empty = False

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def dumps(self):

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        return content
