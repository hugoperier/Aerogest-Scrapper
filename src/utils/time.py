from datetime import datetime
import math

# replace the hour and the minutes of the given date by the given hour and the given minutes
# the "time" expected variable is an integer formated such as hh,mm where minutes are the decimal part from 0 to 0.99
# the date given back is the same date but with the hour and the minutes replaced as well as second and microsecond set to 0
def date_from_flat_hour(date, time):
    return date.replace(hour=math.floor(time), minute= int((time %1) * 60), second=0, microsecond=0)