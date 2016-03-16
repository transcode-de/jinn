from unittest.mock import Mock, PropertyMock

import pytest
from invoke.context import Context


@pytest.fixture
def simple_mock_context():
    """Return a simple Mock object."""
    return Mock(spec=Context)


@pytest.fixture
def mock_context():
    """Return a Mock object with a value attached to a attribute."""
    def get_mock_context(attribute, value):
        mock = Mock(spec=Context)
        setattr(type(mock), attribute, PropertyMock(return_value=value))
        return mock
    return get_mock_context
