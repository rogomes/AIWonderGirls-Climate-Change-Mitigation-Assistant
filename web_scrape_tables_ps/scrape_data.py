import json
import os
import numpy as np
import pandas as pd
import time
# import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_url_contents(data_url):
    html_contents = ""
    try:
        response = urlopen(data_url)  # requests.get(url)
        response_content = response.read()
        html_contents = BeautifulSoup(response_content, "html.parser")
    except Exception as gu:
        print(f"Error accessing site: {data_url}, {gu}")
    return html_contents


def get_all_tables(html_contents, tag):
    tag_contents = html_contents.find_all(tag)
    return tag_contents


def get_header_columns(table_html):
    hdr_columns = []
    table_body = table_html.find('thead')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('th')
        col_texts = [ele.text.strip().replace(u'\xa0', ' ').encode("ascii", "ignore").decode() for ele in cols]
        hdr_columns.append([ele for ele in col_texts if ele])  # Get rid of empty values

    return hdr_columns[0]


def get_table_data(table_html):
    table_data = []
    table_body = table_html.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table_data.append([ele for ele in cols if ele])  # Get rid of empty values

    return table_data


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_data_as(df, table_name, path, file_type):
    if file_type == "csv":
        create_folder(path)
        file_name = os.path.join(path, f"{table_name}" + ".csv")
        df.to_csv(file_name, index=False, header=True)


# extract function
def extract_site_tables(url_links, url_tags, save_path, save_type):
    start = time.time()
    try:
        print(f"Start Extract at {round(start, 2)}...")
        for i in range(len(url_links)):
            url_link = url_links[i]
            url_tag = url_tags[i]
            start_t = time.time()
            print(f"Extracting tables for: \n {url_link} at {round(start_t, 2)}...")
            contents = get_url_contents(url_link)

            if contents is not None:
                tables = get_all_tables(contents, "table")
                if tables is not None:
                    if len(tables) > 0:
                        # find header columns
                        for i in range(len(tables)):
                            curr_table = tables[i]
                            cols = get_header_columns(curr_table)
                            data = get_table_data(curr_table)
                            df = pd.DataFrame(data=data, columns=cols)
                            # print(f"curr data: \n {df.head()}")
                            save_data_as(df, f"{url_tag}_table_{i + 1}", save_path, save_type)
                            print(f"Saved table{i + 1} for {url_tag} in {save_path}")
                            end_time = round(time.time() - start_t, 2)
                            msg = f"Completed extracting tables for: \n {url_link} in {end_time} seconds."
                            print(msg)
        print("Extract completed!")
        total_time = round(time.time() - start, 2)
    except Exception as ee:
        print(f"Error extracting data: {ee}")
    print(f"Total time for all data extraction: {total_time} seconds.")
