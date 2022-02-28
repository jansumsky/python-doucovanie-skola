import csv
import requests
import datetime
CSV_URL_BASE = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

def update_numerical_data(existing_list: list, add_list: list) -> list:
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
            dict_transposed[update_numerical_data(tmp_data, parsed_entry)[idx]] = parsed_entry
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
    CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv'
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

def get_covid_data_month_filtered(month: str, country: str)-> list:
    """

    :param month:
    :param country:
    :return:
    """
    monthly_data = []
    return monthly_data

def get_covid_data_year_filtered(year: str, country: str)-> list:
    """

    :param year:
    :param country:
    :return:
    """
    yearly_data = []
    return yearly_data

if __name__ == '__main__':
    print(get_covid_data_day_filtered("01-01-2021", "Slovakia"))
