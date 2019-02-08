
from .synse_pb2 import V3Tag, V3WriteData


def tag_to_message(tag_string):
    """Convert a tag string to a V3Tag message instance.

    Args:
        tag_string (str): The tag in its string representation.

    Returns:
        V3Tag: The tag string parsed into its proto model.
    """
    # Separate the namespace from the tag if it has one.
    res = tag_string.split('/', maxsplit=1)
    if len(res) == 2:
        ns, tag_string = res[0], res[1]
    else:
        ns, tag_string = '', res[0]

    res = tag_string.split(':', maxsplit=1)
    if len(res) == 2:
        annotation, label = res[0], res[1]
    else:
        annotation, label = '', res[0]

    return V3Tag(
        namespace=ns,
        annotation=annotation,
        label=label,
    )


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
        messages.append(V3WriteData(
            action=payload.get('action') or '',
            data=payload.get('data') or b'',
            transaction=payload.get('transaction') or '',
        ))

    return messages
