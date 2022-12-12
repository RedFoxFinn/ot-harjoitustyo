import datetime

def get_current_date(as_object=False):
    """
    function for creating new timestamp with current date
    
    Args:
      as_object: bool, option to get current date as date object or unix timestamp
    """
    curr = datetime.date.today()
    stamp = datetime.datetime(
        curr.year,
        curr.month,
        curr.day).timestamp()
    return stamp if not as_object else curr

def get_soon_exp_date(days_to_add:int=2):
    """
    function for creating new timestamp with current date and timedelta
    
    Args:
      days_to_add: int, how many days to add to current date
    """
    curr = get_current_date()
    exp_soon = datetime.date.fromtimestamp(curr) + datetime.timedelta(days=days_to_add)
    stamp = datetime.datetime(
        exp_soon.year,
        exp_soon.month,
        exp_soon.day).timestamp()
    return stamp

def get_exp_timestamp(year, month, day):
    """
    function for creating new timestamp from input
    
    Args:
      year: int, year of expiration
      month: int, month of expiration
      day: int, day of expiration
    """
    exp = datetime.datetime(
        year, month, day
    ).timestamp()
    return exp

def expiration_check(timestamp):
    """
    function for checking if expiration date timestamped product has expired
    
    Args:
      timestamp: unix timestamp in seconds, product expiration date
    """
    current = get_current_date()
    if current > timestamp:
        return True
    return False

def expiration_soon_check(timestamp, days_to_add:int=2):
    """
    function for checking if product has expriration date close
    
    Args:
      timestamp: unix timestamp in seconds, product expiration date
      days_to_add: int, how many days to add to current date
    """
    curr = get_current_date()
    exp_soon = get_soon_exp_date(days_to_add)
    if curr <= timestamp and timestamp < exp_soon:
        return True
    return False

def convert_timestamp(timestamp):
    """
    function for returning date object from given timestamp
    
    Args:
      timestamp: unix timestamp in seconds
    """
    obj = datetime.date.fromtimestamp(timestamp)
    return obj