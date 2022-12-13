
from tools.date_tools import expiration_check
from tools.date_tools import expiration_soon_check


def highlight_expired_label(checkup):
    """
    function for returning the text highlight for product rows

    Args:
      checkup: unix timestamp of a product
    """
    expired = expiration_check(checkup)
    expires_soon = expiration_soon_check(checkup)
    if expired:
        return "red"
    if not expired and expires_soon:
        return "orange"
    return "black"
