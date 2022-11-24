import requests
import sqlite3
import pickle
import logging
import argparse
import yaml
from datetime import datetime
from lxml import html
from collections import Counter
from urllib.parse import urlparse


def create_table():
    '''
    create table TAGS if not exist
    :return:
    '''
    sqlite3.register_converter("pickle", pickle.loads)
    conn = sqlite3.connect('tagcounter.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT, date TEXT, taglist pickle)")
    conn.commit()


def add_http_prefix_if_needed(url):
    if not url.startswith("http://"):
        url = "http://" + url
    return url

def parse_html(url):
    '''
    parse html, count tags
    :param url:
    :return:
    '''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    url = add_http_prefix_if_needed(url)

    page = requests.get(url, headers=headers)    # get page by url
    tree = html.fromstring(page.content)    # build tree

    all_elms = tree.cssselect('*')
    all_tags = [x.tag for x in all_elms]    # get tags

    count = Counter(all_tags)   # count tags and save to dictionary
    return dict(count)


def get_name(url):
    '''
    get site name from url
    :param url:
    :return:
    '''
    url = add_http_prefix_if_needed(url)
    t = urlparse(url).netloc
    name = '.'.join(t.split('.')[-2:])
    return name


def save_parsed_tags(url):
    '''
    save url, site name, tag list to the database
    :param url:
    :return:
    '''
    current_datetime = datetime.now()
    dt_string = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    create_table()  # create table in database if not exist
    result = parse_html(url) # parse html, count tags

    conn = sqlite3.connect('tagcounter.db')
    c = conn.cursor()
    for tag in result:
        print('{}: {}'.format(tag, result[tag]))
    string = (get_name(url), url, dt_string, pickle.dumps(result))
    c.execute('''INSERT INTO tags(name, url, date, taglist) VALUES(?, ?, ?, ?)''', string)
    conn.commit()
    logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(asctime)s %(message)s")
    logging.info(f"{url}")

    conn.close()


def get_info_from_db(url):
    '''
    get tag list for url from database
    :param url:
    :return:
    '''
    conn = sqlite3.connect('tagcounter.db')
    c = conn.cursor()
    c.execute("SELECT taglist FROM tags WHERE url = ?", (url,))
    for row in c:
        data = pickle.loads(row[0])
        print(data)
        break
    else:
        print("No info about", url, "in database")
    conn.close()


def select_all_string():
    '''
    just for test
    :param url:
    :return:
    '''
    conn = sqlite3.connect('tagcounter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tags")
    for row in c:
        print(row)
    conn.close()


def drop_all_records():
    '''
    just for test
    :param url:
    :return:
    '''
    conn = sqlite3.connect('tagcounter.db')
    c = conn.cursor()
    c.execute("DROP TABLE tags")
    conn.commit()
    conn.close()


def read_yaml_synonyms(url):
    '''
    define url by synonym from synonyms.yaml
    :param url:
    :return:
    '''
    with open('synonyms.yaml') as f:
        read_data = yaml.load(f, Loader=yaml.FullLoader)

        for read_synonym, read_url in read_data.items():
            if read_synonym == url:
                url = read_url
    return url


def add_synonym(synonym, url):
    '''
    add synonym to the file
    :param synonym:
    :param url:
    :return:
    '''
    to_yaml = {
        synonym: url
    }
    with open('synonyms.yaml', 'a') as f:
        yaml.dump(to_yaml, f)
    print("Synonym", synonym, "for url", url, "added to synonyms.yaml")


def delete_synonym(synonym):
    '''
    remove synonym from file
    :param synonym:
    :return:
    '''
    with open('synonyms.yaml', 'r') as f:   # read file
        read_data = yaml.load(f, Loader=yaml.FullLoader)
    del read_data[synonym]                  # remove synonym
    with open('synonyms.yaml', 'w') as f:   # write down remaining synonyms to the file
        yaml.dump(read_data, f)
    print("Synonym", synonym, "deleted from synonyms.yaml")


def view_synonyms():
    '''
    view synonyms from file
    :return:
    '''
    with open('synonyms.yaml') as f:
        read_data = yaml.load(f, Loader=yaml.FullLoader)
        print(read_data)


def create_parser():
    '''
    parse launch parameters
    :return:
    '''
    parser = argparse.ArgumentParser(prog = 'tagcounter', description='Count tags in html.')
    parser.add_argument('--get', help='get tag list, example: tagcounter --get http://yandex.ru')
    parser.add_argument('--view', help='view saved info about tags from database, example: tagcounter --veiw http://yandex.ru')
    parser.add_argument('--add', nargs='+', help='add synonym to synonyms.yaml, example: tagcounter --add tst http://python.org')
    parser.add_argument('--delete', help='delete synonym from synonyms.yaml example: tagcounter --delete tst')
    parser.add_argument('--synonyms', dest='syn', action='store_true', help='view synonyms.yaml')

    args = parser.parse_args()

    if args.get:
        url = args.get
        url_checked = read_yaml_synonyms(url)
        save_parsed_tags(url_checked)

    if args.view:
        url = args.view
        url_checked = read_yaml_synonyms(url)
        get_info_from_db(url_checked)

    if args.add:
        synonym = args.add[0]
        url = args.add[1]
        add_synonym(synonym, url)

    if args.delete:
        synonym = args.delete
        delete_synonym(synonym)

    if args.syn:
        view_synonyms()


def main():
    create_parser()


if __name__ == '__main__':
    main()
