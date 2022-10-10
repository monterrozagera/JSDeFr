# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from examples import custom_style_2

def printChoicesList(function_format: str, num_choices: int) -> int:
    """ Let the user choose which number will be used for deobfs """
    questions = {
            'type': 'list',
            'name': 'sacrificial_number',
            'message': f'Which argument from {function_format} is used for deobfs? (position)',
            'choices': []
        }

    position = 1
    for n in range(num_choices):
        questions['choices'].append(str(position))
        position += 1

    answers = prompt(questions, style=custom_style_2)
    return str(answers['sacrificial_number'])