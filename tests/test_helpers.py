from jinn import helpers


def test_envdir():
    command = 'python manage.py runserver'
    env = 'prod'
    assert env not in helpers.envdir('', command)
    assert env in helpers.envdir('', command, env)
