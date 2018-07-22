from bs4 import BeautifulSoup
import csv
import requests
import substring

BASE_URL = "https://www.lollapalooza.com/schedule/"
URL_ENDS = ["#thursday-2018-08-02", "#friday-2018-08-03", "#saturday-2018-08-04", "#sunday-2018-08-05"]
END_TAG = ":00-06:00"
artists = []

for i in range (0, 4):
    urlRequest = requests.get(BASE_URL + URL_ENDS[i])
    if i == 0:
        day = "schedule-date-thursday-2018-08-02"
        dateStart = "2018-08-02T"
    elif i == 1:
        day = "schedule-date-friday-2018-08-03"
        dateStart = "2018-08-03T"
    elif i ==2:
        day = "schedule-date-saturday-2018-08-04"
        dateStart = "2018-08-04T"
    else: 
        day = "schedule-date-sunday-2018-08-05"
        dateStart = "2018-08-05T"

    soup = BeautifulSoup(urlRequest.content, 'html5lib')
    table = soup.find('table', attrs = {'id' : day})
    for row in table.findAll('div', attrs = {'class':'o-session__text'}):
        artist = {}
        time = row.find('p', attrs = {'class':'o-session__time'}).text
        timeStart = time.split('-')[0]
        timeEnd = time.split('-')[1]

        if len(timeStart) == 4:
            timeStart = '0' + timeStart
        if len(timeEnd) == 4:
            timeEnd = '0' + timeEnd

        if int(timeStart[:2]) != 12:
            timeStart = str(int(timeStart[:2]) + 12) + timeStart[2:]
        if int(timeEnd[:2]) != 12:
            timeEnd = str(int(timeEnd[:2]) + 12) + timeEnd[2:]

        timeStart = dateStart + timeStart + END_TAG
        timeEnd = dateStart + timeEnd + END_TAG

        artist['artist'] = row.find('p', attrs = {'class':'o-session__title'}).text
        artist['startTime'] = timeStart
        artist['endTime'] = timeEnd
        artists.append(artist)

filename = 'artists.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f, ['artist','startTime', 'endTime'])
    w.writeheader()
    for artist in artists:
        w.writerow(artist)