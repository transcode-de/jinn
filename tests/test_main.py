from jinn import main, tasks


def test_main():
    assert main.program.namespace.tasks == tasks.ns.tasks
