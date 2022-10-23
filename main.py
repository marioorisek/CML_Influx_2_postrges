from influxdb import InfluxDBClient
import dotenv
from datetime import datetime
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

dotenv.load_dotenv()

db = InfluxDBClient(host="192.168.10.124")

def read_metric(database, channel_name, metric, time_frame="24h"):
    try:
        result = db.query(f"SELECT {metric}(*) FROM {database}..{channel_name} WHERE time > now() - {time_frame}")
        result = result.raw["series"][0]["values"][0][1]
        return result
    except:
        return -255

def read_avg(database, channel_name):
    try:
        result = db.query(f"SELECT MEAN(*) FROM {database}..{channel_name}")
        result = result.raw["series"][0]["values"][0][1]
        return result
    except:
        return -255

def read_24h_spread(database, channel_name):
    return(read_metric(database, channel_name, "SPREAD"))

def read_18h_min(database, channel_name):
    return(read_metric(database, channel_name, "MIN", time_frame='18h'))

def read_24h_max(database, channel_name):
    return(read_metric(database, channel_name, "MAX"))

def read_last(database, channel_name):
    return(read_metric(database, channel_name, "LAST"))

output_message_text = f"{datetime.now().strftime('%a %b %d %Y, %H:%M:%S')}\n{15*'-'}\n"

output_message_text += "Teplota venku:\n"

result = read_last(channel_name="venku_teplota", database="doom")
output_message_text += f"aktuální: {result:,.1f} °C. \n"

result = read_18h_min(channel_name="venku_teplota", database="doom")
output_message_text += f"minimální: {result:,.1f} °C. \n"

result = read_avg(channel_name="venku_teplota", database="doom")
output_message_text += f"průměrná: {result:,.1f} °C.\n"

result = read_24h_max(channel_name="venku_teplota", database="doom")
output_message_text += f"maximální: {result:,.1f} °C.\n"

output_message_text += f"{15*'-'}\n"

result = read_24h_spread(channel_name="prepad_vrtu_absolut", database="doom")
output_message_text += f"Za poslednich 24 hodin přeteklo: {result:,.0f} l vody. \n"

output_message_text += f"{15*'-'}\n"

result = read_24h_spread(channel_name="prizemi_celkova_spotreba", database="spotreba_elektriny") / 1000
output_message_text += f"Za posledních 24 hodin spotřebováno: {result:,.2f} kWh elektřiny.\n"

# result = read_24h_spread(channel_name="dum_celkova_spotreba", database="spotreba_elektriny") / 1000
# output_message_text += f"Spotreba eletriny domu za poslednich 24 hodin: {result:,.1f} kWh.\n"
#
# result = read_24h_spread(channel_name="dilna_celkova_spotreba", database="spotreba_elektriny") / 1000
# output_message_text += f"Spotreba eletriny dilna za poslednich 24 hodin: {result:,.1f} kWh.\n"

print(output_message_text)

# mail_list = ['horky.lukas@gmail.com', 'nada.horka@google.com']

mail_list = ['horky.lukas@gmail.com']

for to in mail_list:
    mail = Mail(from_email='cml@horky.tech',
                to_emails=to,
                subject='Domácí sumář',
                plain_text_content=output_message_text
                )
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(mail)
    except Exception as e:
        print(e.message)