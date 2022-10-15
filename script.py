from pathlib import Path
from geopy.geocoders import Nominatim
import requests
import pandas as pd


class CityNotFoundError(Exception):
    def _init_(self, msg):
        super()._init_(msg)


class ForecastUnavailable(Exception):
    def _init_(self, msg):
        super()._init_(msg)


def get_forecast(city='Pittsburgh'):
    geolocator = Nominatim(user_agent="ssarwari")
    location = geolocator.geocode(city)
    if location==None:
        raise CityNotFoundError("Latitude and Longitude unavailable.")
        return
    
    lats = location.latitude
    longs = location.longitude

    if (lats is None) or (longs is None):
        raise CityNotFoundError("Latitude and Longitude unavailable.")
        return

    url = f'https://api.weather.gov/points/{lats},{longs}'
    response = requests.get(ur;)
    if (response.status_code != 200):
        raise ForecastUnavailable("Status code unsuccessful.")
        return

    url2 = response.json()['properties']['forecast']
    response2 = requests.get(url2)
    info = response2.json()['properties']['periods']

    for i in range(len(info)):
        if (info[i]["name"] == "Tonight"):
            start_time = info[i]['startTime']
            end_time = info[i]['endTime']
            detailed_forecast = info[i]['detailedForecast']

    period = {"startTime": start_time,
              "endTime": end_time,
              "detailedForecast": detailed_forecast}
    return period


def main():
    period = get_forecast()

    file = 'weather.pkl'

    if Path(file).exists():
        df = pd.read_pickle(file)
    else:
        df = pd.DataFrame(columns=['Start Date', 'End Date', 'Forecast'])

    df = df.append({'Start Date': period['startTime'],
                    'End Date': period['endTime'],
                    'Forecast': period['detailedForecast']},
                   ignore_index=True)
    df = df.drop_duplicates()
    df.to_pickle(file)

    '''sort repositories'''
    file = open("README.md", "w")
    file.write('![Status](https://github.com/sarwarisak/python-' +
               'get-forecast/actions/workflows/build.yml/badge.svg)\n')
    file.write('![Status](https://github.com/sarwarisak/python-' +
               'get-forecast/actions/workflows/pretty.yml/badge.svg)\n')
    file.write('# Pittsburgh Nightly Forecast\n\n')

    file.write(df.to_markdown(tablefmt='github'))
    file.write('\n\n---\nCopyright © 2022 Pittsburgh ' +
               'Supercomputing Center. All Rights Reserved.')
    file.close()


if __name__ == "__main__":
    main()
