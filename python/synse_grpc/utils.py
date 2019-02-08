
from synse_grpc.synse_pb2 import V3Tag


def str_to_tag(tag_string):
    """Convert a tag string to a V3Tag instance.

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
