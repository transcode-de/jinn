from invoke import Program
from invoke import Collection
from . import tasks


program = Program(namespace=Collection.from_module(tasks), version='0.1.0')
