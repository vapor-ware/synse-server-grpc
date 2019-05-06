
import re

from google.protobuf.json_format import MessageToDict

from synse_grpc.synse_pb2 import HealthStatus, V3Tag, V3WriteData, WriteStatus

# Precompile regexes for dict key CamelCase to snake_case conversion
_re_first = re.compile('(.)([A-Z][a-z]+)')
_re_all = re.compile('([a-z0-9])([A-Z])')


def to_dict(obj):
    """Convert a gRPC message to its dictionary representation.

    Args:
        obj: The gRPC message to convert to dict.

    Returns:
        dict: A dictionary representation of the message.
    """
    d = MessageToDict(obj, including_default_value_fields=True)
    response = {}
    for key, value in d.items():
        # This check is a bit of a hack to ensure that the []byte encoded
        # in the V3WriteData's `data` field does not get serialized out
        # when MessageToDict is called.
        if isinstance(obj, V3WriteData) and key == 'data':
            response[key] = obj.data
            continue
        new_key = _re_all.sub(r'\1_\2', _re_first.sub(r'\1_\2', key)).lower()
        response[new_key] = value

    return response


def tag_to_message(tag):
    """Convert a tag string to a V3Tag message instance.

    Args:
        tag (str): The tag in its string representation.

    Returns:
        V3Tag: The tag string parsed into its proto model.
    """
    # Separate the namespace from the tag if it has one.
    res = tag.split('/', maxsplit=1)
    if len(res) == 2:
        ns, tag = res[0], res[1]
    else:
        ns, tag = '', res[0]

    res = tag.split(':', maxsplit=1)
    if len(res) == 2:
        annotation, label = res[0], res[1]
    else:
        annotation, label = '', res[0]

    return V3Tag(
        namespace=ns,
        annotation=annotation,
        label=label,
    )


def tag_string(message):
    """Convert a gRPC V3Tag message to its corresponding tag string.

    Args:
        message (V3Tag): The tag message to convert to its string representation.

    Returns:
        str: The string representation of the tag message.
    """
    tag = ''

    if message.namespace:
        tag += f'{message.namespace}/'
    if message.annotation:
        tag += f'{message.annotation}:'
    tag += message.label

    return tag


def write_data_to_messages(data):
    """Convert the data to V3WriteData message instance(s).

    Args:
        data (list[dict] | dict): A dictionary or list of dictionaries
            which contain the POSTed write payload. This will be
            converted to gRPC message(s).

    Returns:
        list[V3WriteData]: The write data formatted into gRPC message(s).
    """
    if isinstance(data, dict):
        data = [data]

    messages = []
    for payload in data:
        # Data is expected as bytes. If it is a string, encode it as bytes.
        d = payload.get('data', b'')
        if isinstance(d, str):
            d = d.encode()

        messages.append(V3WriteData(
            action=payload.get('action', ''),
            data=d,
            transaction=payload.get('transaction', ''),
        ))

    return messages


def write_status_name(value):
    """Get the name for a given write status value.

    Args:
        value (int): The value representing the write status.

    Returns:
        str: The string representation of the write status.
    """
    return WriteStatus.Name(value).lower()


def health_status_name(value):
    """Get the name for the given health status value.

    Args:
        value (int): The value representing the health status.

    Returns:
        str: The string representation of the health status.
    """
    return HealthStatus.Name(value).lower()
