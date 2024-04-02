import pytz
from datetime import datetime

#Timezone
def get_current_time():
    desired_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    current_timestamp = datetime.now(desired_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return ('['+ current_timestamp +']')
