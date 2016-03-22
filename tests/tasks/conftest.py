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


@pytest.fixture
def complex_context():
    """Return a Mock object with all attributes and values attached."""
    def get_complex_context(attribut_value_pairs):
        mock = Mock(spec=Context)
        for attribute, value in attribut_value_pairs:
            setattr(type(mock), attribute, PropertyMock(return_value=value))
        return mock
    return get_complex_context
