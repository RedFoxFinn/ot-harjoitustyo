
import re


def selector_type_validation_for_ingredient(selected_type):
    res = re.search("Raaka-aineet", selected_type)
    return bool(res)
