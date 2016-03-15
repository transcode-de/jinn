from invoke import Collection, Program
from invoke.parser import ParserContext

from jinn import tasks


class MyProgram(Program):
    """Until the problem with https://github.com/pyinvoke/invoke/issues/283
    is fixed we need this work around class and property.
    """
    @property
    def initial_context(self):
        args = super().core_args()
        args += super().task_args()
        return ParserContext(args=args)

program = MyProgram(namespace=Collection.from_module(tasks), version='0.1.0')
