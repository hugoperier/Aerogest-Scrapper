from datetime import datetime

def email_format(reservations):
    today = datetime.now()
    message = f"        <h2>{today.strftime('%A %d %B %Y')}</h2>\n"
    for reservation in reservations:
        message += f"        <div class=\"reservation\">\n"
        message += f"            <h3>{reservation['instructor'].trigram}</h3>\n"
        message += f"            <p>{reservation['airplane'].registration}</p>\n"
        message += f"            <p>{reservation['schedule']['start'].strftime('%H:%M')} - {reservation['schedule']['end'].strftime('%H:%M')}</p>\n"
        message += f"        </div>\n"
    return message

def text_format(reservations):
    message = f"[{datetime.now().strftime('%H:%M:%S')}]  Found {len(reservations)} matches:\n"
    for reservation in reservations:
        message += f"{reservation['schedule']['start'].strftime('%d/%m/%Y')} {reservation['instructor'].trigram} - {reservation['airplane'].registration} {reservation['schedule']['start'].strftime('%H:%M')} - {reservation['schedule']['end'].strftime('%H:%M')}\n"
    return message