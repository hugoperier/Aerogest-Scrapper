from datetime import datetime

def formatReservations(reservations):
    today = datetime.now()
    message = f"        <h2>{today.strftime('%A %d %B %Y')}</h2>\n"
    for reservation in reservations:
        message += f"        <div class=\"reservation\">\n"
        message += f"            <h3>{reservation['instructor'].trigram}</h3>\n"
        message += f"            <p>{reservation['airplane'].registration}</p>\n"
        message += f"            <p>{reservation['schedule']['start'].strftime('%H:%M')} - {reservation['schedule']['end'].strftime('%H:%M')}</p>\n"
        message += f"        </div>\n"
    return message
