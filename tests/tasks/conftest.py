from unittest.mock import MagicMock, Mock

import pytest
from invoke.config import Config
from invoke.context import Context

from jinn import tasks


@pytest.fixture
def simple_mock_context():
    """Return a simple Mock object."""
    return Mock(spec=Context)


@pytest.fixture
def mock_context():
    '''Return module specific context with mocked run method'''
    def get_mock_context(module=None):
        # extend module config with general config
        if module is not None:
            module.ns.configure(tasks.jinn_config)
            context = Context(config=Config(overrides=module.ns._configuration))
        else:
            context = Context(config=Config(overrides=tasks.jinn_config))
        context.run = MagicMock()
        return context
    return get_mock_context
