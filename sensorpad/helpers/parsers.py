from dateutil import parser


def isoformat_parser(timestamp_in_isoformat):
    """Parse timestamp in isoformat."""
    try:
        result = parser.isoparse(timestamp_in_isoformat)
    except (ValueError, TypeError):
        result = None
    return result
