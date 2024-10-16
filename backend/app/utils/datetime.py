import datetime

def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc)

def get_current_date():
    return datetime.datetime.now(datetime.timezone.utc).date()
