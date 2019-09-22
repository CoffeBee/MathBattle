from .models import Task
from sympy import simplify, cos, sin, expand, symbols, init_printing


class Checker():
    def __init__(self, right_answer, typetype):
        self.right_answer = right_answer
        self.listOfNums = []
        self.typetype = typetype

    def check(self, answer):
        '''
        try:
            Tasks = Task.objects.all()
            typytype = self.typetype
            rans = self.right_answer
            x, y, z = symbols('x y z')
            init_printing(use_unicode=True)
            eval_str = 'simplify(({})-({}))'.format(rans, answer)
            if (eval(eval_str) == 0):
                return "OK"
            else:
                return "WA"
        except Exception as e:
            print(e)
            return "CF"
        '''
        Tasks = Task.objects.all()
        typytype = self.typetype
        rans = self.right_answer
        x, y, z = symbols('x y z')
        init_printing(use_unicode=True)
        eval_str = 'simplify(({})-({}))'.format(rans, answer)
        if (eval(eval_str) == 0):
             return "OK"
        else:
             return "WA"
