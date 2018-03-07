# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
# import subprocess
# import errno
from pylatex.base_classes import Environment, Command, Container, LatexObject, UnsafeCommand, CommandBase
# from pylatex.base_classes.command import Arguments,CommandBase
from pylatex.package import Package
from pylatex.utils import dumps_list, rm_temp_dir, NoEscape
import pylatex.config as cf
# from json import *
import random
import json


class LatexSnippt(Environment):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dumps(self):

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        return content
