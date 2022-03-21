import csv
import requests
import datetime

import matplotlib.pyplot as plt
import numpy as np
CSV_URL_BASE = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

def get_timestamps(start_date: str = datetime.date.today(), day_count: int=7):
    timestamps = []
    if start_date != datetime.date.today():
        start_date = datetime.datetime.strptime(start_date, '%Y-%M-%d')

    day_delta = datetime.timedelta(days=1)
    end_date = start_date + day_count * day_delta
    for i in range((end_date - start_date).days):
       timestamps.append(str(start_date + i * day_delta).split(" ")[0])
    return timestamps

def visualize_data(data, timespan):
    x = timespan
    y1, y2, y3, y4 = [], [], [], []
    plt.rcParams['figure.figsize'] = (10, 13)
    for entry in data:
        y1.append(entry[7])
        y2.append(entry[8])
        y3.append(entry[9])
        y4.append(entry[10])
    plot1 = plt.figure(1)

    plt.subplot(221)
    plt.plot(x, y1)
    plt.xticks(rotation=45)

    plt.subplot(222)
    plt.plot(x, y2)
    plt.xticks(rotation=45)

    plt.subplot(223)
    plt.plot(x, y3)
    plt.xticks(rotation=45)

    plt.subplot(224)
    plt.plot(x, y4)
    plt.xticks(rotation=45)

    plt.show()


def update_numerical_data(existing_list: list, add_list: list)-> list:
    """
    Updates existing list with defined fields of add_list
    :param existing_list: base list
    :param add_list: list to be added
    :return: updated data
    """
    try:
        combined_list = existing_list
        combined_list[7] = str(int(combined_list[7]) + int(add_list[7]))
        combined_list[8] = str(int(combined_list[8]) + int(add_list[8]))
        combined_list[9] = str(int(combined_list[9]) + int(add_list[9]))
        combined_list[10] = str(int(combined_list[10]) + int(add_list[10]))
    except ValueError:
        print(existing_list)
        print(add_list)
        exit(1)
    return combined_list


def transpose_by_idx(covid_data: list, idx: int)-> dict:
    """
    Transposes data from list to dict with selectable index
    :param covid_data: raw input as a list
    :param idx: [2: Province, 3: Country, 11: Combined]
    :return: dictionary
    """
    dict_transposed = {}
    for parsed_entry in covid_data:
        if dict_transposed.get(parsed_entry[idx]):
            tmp_data = dict_transposed.get(parsed_entry[idx])
            dict_transposed[parsed_entry[idx]] = update_numerical_data(tmp_data, parsed_entry)
        else:
            dict_transposed.update({parsed_entry[idx]: parsed_entry})
    return dict_transposed


def get_covid_data_for_day(day: str, group_by: int) -> dict:
    """
    Return Daily data as a dictionary
    :param day: string in format: DD-MM-YYYY
    :param group_by: [2: Province, 3: Country, 11: Combined]
    :return: dict of transposed data
    """
    s = requests.Session()
    download = s.get(CSV_URL_BASE + day + ".csv")
    reader = csv.reader(download.content.decode('utf-8').strip().split("\n"),delimiter = ",")
    decoded_content = list(reader)
    transposed_content = transpose_by_idx(decoded_content, group_by)
    return transposed_content


def get_covid_data_day_filtered(day: str, country: str)-> list:
    """
    Return Daily data as a list for a selected country
    :param day: string in format: DD-MM-YYYY
    :param country: String name of country eg. Slovakia
    :return: list of actual data
    """
    data = get_covid_data_for_day(day, 3)
    return data[country]

def get_covid_data_filtered_timespan(country: str, start_date: str, timespan: int)-> list:
    """

    :param month:
    :param country:
    :param start_date:
    :param timespan:
    :return:
    """
    monthly_data = []
    for date in get_timestamps(start_date, timespan):
        tmp_date = datetime.datetime.strptime(date, "%Y-%m-%d" ).strftime("%m-%d-%Y")
        print(tmp_date)
        monthly_data.append(get_covid_data_day_filtered(tmp_date, country))
    visualize_data(monthly_data, get_timestamps(start_date, timespan))





if __name__ == '__main__':
    get_covid_data_filtered_timespan("Slovakia", "2021-01-01", 7)