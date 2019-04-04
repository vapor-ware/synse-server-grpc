
import pytest

from synse_grpc import utils
from synse_grpc.api import V3Tag, V3WriteData


@pytest.mark.parametrize('tag,message', [
    ('vapor/foo:bar', V3Tag(namespace='vapor', annotation='foo', label='bar')),
    ('foo:bar', V3Tag(annotation='foo', label='bar')),
    ('vapor/bar', V3Tag(namespace='vapor', label='bar')),
    ('bar', V3Tag(label='bar')),
])
def test_tag_to_message(tag, message):
    """Test converting a tag string to the V3Tag message."""

    assert utils.tag_to_message(tag) == message


@pytest.mark.parametrize('data,messages', [
    (
        {'action': 'foo'},
        [V3WriteData(action='foo')]
    ),
    (
        {'action': 'foo', 'data': b'bar'},
        [V3WriteData(action='foo', data=b'bar')]
    ),
    (
        {'action': 'foo', 'data': b'bar', 'transaction': '123'},
        [V3WriteData(action='foo', data=b'bar', transaction='123')]
    ),
    (
        {'action': 'foo', 'transaction': '123'},
        [V3WriteData(action='foo', transaction='123')]
    ),
    (
        [{'action': 'foo'}],
        [V3WriteData(action='foo')]
    ),
    (
        [{'action': 'foo', 'data': b'bar'}],
        [V3WriteData(action='foo', data=b'bar')]
    ),
    (
        [{'action': 'foo', 'data': b'bar', 'transaction': '123'}],
        [V3WriteData(action='foo', data=b'bar', transaction='123')]
    ),
    (
        [{'action': 'foo', 'transaction': '123'}],
        [V3WriteData(action='foo', transaction='123')]
    ),
    (
        [
            {'action': 'foo'},
            {'action': 'abc'}
        ],
        [
            V3WriteData(action='foo'),
            V3WriteData(action='abc'),
        ]
    ),
    (
        [
            {'action': 'foo', 'data': b'bar'},
            {'action': 'abc'}
        ],
        [
            V3WriteData(action='foo', data=b'bar'),
            V3WriteData(action='abc'),
        ]
    ),
    (
        [
            {'action': 'foo', 'data': b'bar', 'transaction': '123'},
            {'action': 'abc'}
        ],
        [
            V3WriteData(action='foo', data=b'bar', transaction='123'),
            V3WriteData(action='abc'),
        ]
    ),

])
def test_write_data_to_message(data, messages):
    """Test converting some write data to a V3WriteData message."""

    assert utils.write_data_to_messages(data) == messages
