from abc import ABCMeta
from dataclasses import asdict
from datetime import datetime


def transform_parameter_dict(parameters):
    new_param_dict = {}
    for group in parameters:
        if type(group['value']) == list:
            # if group['variable'] == "monitoring":
            #     new_param_dict[group['variable']] = group['value']
            # else:
            new_param_dict[group['variable']] = transform_parameter_dict(group['value'])
        else:
            new_param_dict[group['variable']] = group['value']

    return new_param_dict


def transform_dataclass_to_dict(dataclass_object):
    if type(type(dataclass_object)) == ABCMeta:
        dataclass_object = asdict(dataclass_object)

    new_dict = {}
    for key, value in dataclass_object.items():
        # print(type(key))
        if type(value) == dict or type(type(value)) == ABCMeta:
            new_dict[str(key)] = transform_dataclass_to_dict(value)
        else:
            # print("Done: ", value)
            if isinstance(value, datetime):
                new_dict[str(key)] = str(value.isoformat())
            elif isinstance(value, datetime):
                new_dict[str(key)] = str(value)
            elif is_number(str(value)):
                new_dict[str(key)] = value
            else:
                new_dict[str(key)] = str(value)

    return new_dict


def is_number(s):
    # Source: https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
