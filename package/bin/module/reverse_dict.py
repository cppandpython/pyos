from ..sys.error import invalid_type


def reverse_dict(d):
    invalid_type('d', d, dict)

    return {value: key for (key, value) in d.items()}