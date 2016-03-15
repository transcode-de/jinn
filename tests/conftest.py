from unittest.mock import Mock

import pytest
from invoke.context import Context


@pytest.fixture
def mock_context():
    return Mock(spec=Context)
