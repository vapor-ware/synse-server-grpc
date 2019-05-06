
import pytest

from synse_grpc import api, utils


@pytest.mark.parametrize('message,expected', [
    (
        api.V3Tag(
            namespace='vapor',
            label='foo',
        ),
        {
            'namespace': 'vapor',
            'annotation': '',
            'label': 'foo',
        },
    ),
    (
        api.V3WriteData(
            action='foo',
            data=b'bar',
        ),
        {
            'action': 'foo',
            'data': b'bar',
            'transaction': '',
        },
    ),
    (
        api.V3Reading(
            id='123',
            string_value='foo',
            type='test',
            unit=api.V3OutputUnit(
                name='test',
                symbol='T',
            ),
        ),
        {
            'id': '123',
            'timestamp': '',
            'type': 'test',
            'device_type': '',
            'string_value': 'foo',
            'unit': {
                'name': 'test',
                'symbol': 'T',
            },
            'context': {},
        },
    ),
    (
        api.V3TransactionStatus(
            id='123',
            timeout='5s',
            status=api.DONE,
        ),
        {
            'id': '123',
            'created': '',
            'updated': '',
            'message': '',
            'timeout': '5s',
            'status': 'DONE',
        },
    ),
])
def test_to_dict(message, expected):
    """Convert gRPC messages to their dictionary representations."""

    assert utils.to_dict(message) == expected


@pytest.mark.parametrize('tag,message', [
    ('vapor/foo:bar', api.V3Tag(namespace='vapor', annotation='foo', label='bar')),
    ('foo:bar', api.V3Tag(annotation='foo', label='bar')),
    ('vapor/bar', api.V3Tag(namespace='vapor', label='bar')),
    ('bar', api.V3Tag(label='bar')),
    ('', api.V3Tag()),
])
def test_tag_to_message(tag, message):
    """Convert a tag string to the V3Tag message."""

    assert utils.tag_to_message(tag) == message


@pytest.mark.parametrize('tag,string', [
    (api.V3Tag(), ''),
    (api.V3Tag(label='foo'), 'foo'),
    (api.V3Tag(namespace='vapor', label='foo'), 'vapor/foo'),
    (api.V3Tag(namespace='vapor', annotation='bar', label='foo'), 'vapor/bar:foo'),
    (api.V3Tag(annotation='bar', label='foo'), 'bar:foo'),
])
def test_tag_string(tag, string):
    """Convert a V3Tag to its corresponding tag string."""

    assert utils.tag_string(tag) == string


@pytest.mark.parametrize('data,messages', [
    (
        {},
        [api.V3WriteData()]
    ),
    (
        [{}],
        [api.V3WriteData()]
    ),
    (
        {'action': 'foo'},
        [api.V3WriteData(action='foo')]
    ),
    (
        {'action': 'foo', 'data': 'bar'},
        [api.V3WriteData(action='foo', data=b'bar')]
    ),
    (
        {'action': 'foo', 'data': b'bar'},
        [api.V3WriteData(action='foo', data=b'bar')]
    ),
    (
        {'action': 'foo', 'data': b'bar', 'transaction': '123'},
        [api.V3WriteData(action='foo', data=b'bar', transaction='123')]
    ),
    (
        {'action': 'foo', 'transaction': '123'},
        [api.V3WriteData(action='foo', transaction='123')]
    ),
    (
        [{'action': 'foo'}],
        [api.V3WriteData(action='foo')]
    ),
    (
        [{'action': 'foo', 'data': b'bar'}],
        [api.V3WriteData(action='foo', data=b'bar')]
    ),
    (
        [{'action': 'foo', 'data': b'bar', 'transaction': '123'}],
        [api.V3WriteData(action='foo', data=b'bar', transaction='123')]
    ),
    (
        [{'action': 'foo', 'transaction': '123'}],
        [api.V3WriteData(action='foo', transaction='123')]
    ),
    (
        [
            {'action': 'foo'},
            {'action': 'abc'}
        ],
        [
            api.V3WriteData(action='foo'),
            api.V3WriteData(action='abc'),
        ]
    ),
    (
        [
            {'action': 'foo', 'data': b'bar'},
            {'action': 'abc'}
        ],
        [
            api.V3WriteData(action='foo', data=b'bar'),
            api.V3WriteData(action='abc'),
        ]
    ),
    (
        [
            {'action': 'foo', 'data': b'bar', 'transaction': '123'},
            {'action': 'abc'}
        ],
        [
            api.V3WriteData(action='foo', data=b'bar', transaction='123'),
            api.V3WriteData(action='abc'),
        ]
    ),

])
def test_write_data_to_message(data, messages):
    """Convert some write data to a V3WriteData message."""

    assert utils.write_data_to_messages(data) == messages


@pytest.mark.parametrize('status,name', [
    (0, 'pending'),
    (1, 'writing'),
    (3, 'done'),
    (4, 'error'),
])
def test_write_status_name(status, name):
    """Get the name for the write status value."""

    assert utils.write_status_name(status) == name


def test_write_status_name_error():
    """Get the name for an invalid write status value."""

    with pytest.raises(ValueError):
        utils.write_status_name(-1)


@pytest.mark.parametrize('status,name', [
    (0, 'unknown'),
    (1, 'ok'),
    (2, 'failing'),
])
def test_health_status_name(status, name):
    """Get the name for the health status value."""

    assert utils.health_status_name(status) == name


def test_health_status_name_error():
    """Get the name for an invalid health status value."""

    with pytest.raises(ValueError):
        utils.health_status_name(-1)
