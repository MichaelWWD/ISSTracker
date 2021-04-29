import requests
from datetime import datetime
import smtplib
import time
sender = "dimeji_mike@yahoo.com"
gm_password = "Galahad12"
y_password = "hmwohcwefthricib"
receiver = 'dimejimike9@gmail.com'

MY_LAT = 6.548620   # Your latitude
MY_LONG = 3.364490  # Your longitude


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_latitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_overhead() and is_night():
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=sender, password=y_password)
            connection.sendmail(
                from_addr=sender,
                to_addrs=receiver,
                msg=f"Subject:Look up\n\nISS is above you "
            )
