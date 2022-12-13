
def build_elements_for_selector(list_of=None, for_type=True):
    """
    function for building elements for type or subtype selector dropdown
    in AddProduct section of the UI

    Args:
      list_of: list, list of types or subtypes in database
      for_type: bool, True if for types, False for subtypes
    """
    _type_default = [f"{0:02d} - valitse tyyppi"]
    _subtype_default = [f"{0:02d} - valitse alatyyppi"]
    if for_type:
        options = _type_default + [f"{t[1]:02d} - {t[0]}" for t in list_of] if \
            list_of is not None else _type_default
    else:
        options = _subtype_default + [f"{s[2]:02d} - {s[1]}" for s in list_of] if \
            list_of is not None else _subtype_default
    return options


def build_id_from_selector_number(selector_number_str: str):
    """
    function for building type or subtype id from selected selector element

    Args:
      selector_number_str: str, part (first two characters) of selector element string
    """
    first = selector_number_str[0]
    second = selector_number_str[1]
    if first == '0':
        return int(f"{second}")
    return int(f"{first}{second}")
