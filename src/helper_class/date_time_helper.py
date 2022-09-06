import pytz
from datetime import datetime

def get_update_time():
    time_zone = pytz.timezone('Europe/Madrid')
    last_time_update = datetime.now(time_zone)
    return last_time_update.strftime("%Y-%m-%d %H:%M:%S")