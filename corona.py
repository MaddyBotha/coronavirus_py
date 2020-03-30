from win10toast import ToastNotifier
from bs4 import BeautifulSoup
import requests
import time

country = "South Africa"
notification_duration = 10
refresh_time = 1  # minutes
data_check = []
worldmetersLink = "https://www.worldometers.info/coronavirus/"


def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("+", "")
        i = i.replace("-", "")
        i = i.replace(",", ".")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L


while True:
    try:
        html_page = requests.get(worldmetersLink)
    except requests.exceptions.RequestException as e:
        print(e)
        continue
    bs = BeautifulSoup(html_page.content, 'html.parser')

    search = bs.select("div tbody tr td")
    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(country) != -1:
            start = i
            break
    data = []
    for i in range(1, 8):
        try:
            data = data + [search[start+i].get_text()]
        except:
            data = data + ["0"]

    data = data_cleanup(data)
    message = "Infected = {}, New = {}, Deaths = {}, Recovered = {}, Active = {}, Critical = {}".format(
        *data)

    if data_check != data:
        data_check = data
        toaster = ToastNotifier()
        toaster.show_toast("Coronavirus {}".format(
            country), message, duration=notification_duration)
    else:
        time.sleep(refresh_time*60)
        continue


# Thanks to : Khelifi Ahmed Aziz for the tutorial and https://towardsdatascience.com/coronavirus-track-coronavirus-in-your-country-by-displaying-notification-c914b5652088
