
import pytest

from synse_grpc import utils
from synse_grpc.api import V3Tag


@pytest.mark.parametrize('tag,expected', [
    ('vapor/foo:bar', V3Tag(namespace='vapor', annotation='foo', label='bar')),
    ('foo:bar', V3Tag(annotation='foo', label='bar')),
    ('vapor/bar', V3Tag(namespace='vapor', label='bar')),
    ('bar', V3Tag(label='bar')),
])
def test_str_to_tag(tag, expected):
    """Test converting a tag string to the V3Tag message."""

    assert utils.str_to_tag(tag) == expected
