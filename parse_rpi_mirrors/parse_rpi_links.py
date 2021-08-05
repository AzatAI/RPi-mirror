from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


URL = f'https://www.raspbian.org/RaspbianMirrors'


def clean_link(link_s):
    match = re.search(r'href=[\'"]?([^\'" >]+)', link_s)
    if match:
        return match.group(1)
    else:
        elements = link_s.strip().replace("</p><", "").replace("<br/>", "").replace("rsync", "").replace("(ftp|)", "").split("://")
        if len(elements) > 1:
            return "http://" + elements[1].strip()


def get_links(html, HEADER, URL):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    table_ls = table.findAll("tr")
    links = []
    for index in range(0, len(table_ls)):
        link = (str(table_ls[index]).split("/td")[3][25:len(str(table_ls[index]))])
        link = clean_link(link)
        if link:
            links.append(link)
    return links


def get_html(url, HEADERS, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def write_links(links):
    with open("mirrors.txt", "w") as file:
        for link in links:
            file.write(f"{link}\n")


def main():
    main_html = get_html(URL, HEADERS, None)

    if main_html.status_code == 200:
        parsed_links = get_links(main_html.text, HEADERS, URL)

        write_links(parsed_links)

main()
