def clean_dict(dictionary):
    """
    Returns a new but cleaned dictionary.

    * Keys with None type values are removed
    * Keys with empty string values are removed

    This function is designed so we only return useful data
    """

    newdict = dict(dictionary)
    for key in dictionary.keys():
        if dictionary.get(key) is None:
            del newdict[key]
        if dictionary[key] == "":
            del newdict[key]
    return newdict


def clean_list(lst):
    """
    Returns a new but cleaned list.

    * None type values are removed
    * Empty string values are removed

    This function is designed so we only return useful data
    """
    newlist = list(lst)
    for i in lst:
        if i is None:
            newlist.remove(i)
        if i == "":
            newlist.remove(i)
    return newlist


def clean(obj):
    """
    Returns a new but cleaned JSON object.

    * Recursively iterates through the collection
    * None type values are removed
    * Empty string values are removed

    This function is designed so we only return useful data
    """

    cleaned = clean_list(obj) if isinstance(obj, list) else clean_dict(obj)

    # The only *real* difference here is how we have to iterate through these different collection types
    if isinstance(cleaned, list):
        for key, value in enumerate(cleaned):
            if isinstance(value, list) or isinstance(value, dict):
                cleaned[key] = clean(value)
    elif isinstance(cleaned, dict):
        for key, value in cleaned.items():
            if isinstance(value, dict) or isinstance(value, list):
                cleaned[key] = clean(value)

    return cleaned
