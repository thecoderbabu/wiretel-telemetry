import csv, os, re
import argparse
from pages.login_page import LoginPage, InvalidTagForAuthorError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import local_config as config
from send_mail import send_mail
from datetime import datetime


def get_args():
    parser = argparse.ArgumentParser(description="Get args")
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        required=False,
        help='Run when forced'
    )
    return parser.parse_args()


def convert_to_gb(list_of_usage):
    gb = []
    mb = []
    bts = []
    gb_pattern = r"(\d+) GB"
    mb_pattern = r"(\d+) MB"
    bts_pattern = r"(\d+) Bytes"

    for usage in list_of_usage:
        gb_match = re.search(gb_pattern, usage)
        mb_match = re.search(mb_pattern, usage)
        bts_match = re.search(bts_pattern, usage)
        if gb_match:
            gb.append(int(gb_match.group(1)))
        if mb_match:
            mb.append(int(mb_match.group(1)))
        if bts_match:
            bts.append(int(bts_match.group(1)))
    total_gb = sum(gb) + sum(mb) / 1024 + sum(bts) / 1024 / 1024 / 1024
    return total_gb


args = get_args()
if not args.force:
    try:

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service(config.DRIVER_PATH)
        chrome = webdriver.Chrome(service=service, options=options)
        chrome.maximize_window()
        chrome.get("https://my.wiretel.in/login/index")
        page = LoginPage(chrome)

        list1 = []
        dict1 = {}
        head, table_data1 = page.input_form(config.USERNAME, config.PASSWORD)
        for row in head:
            dict1[row] = []
        list1.append(head)
        list1 += table_data1
        print("Table_data1 :", len(table_data1))

        for row in list1[1:]:
            for i in range(len(row)):
                dict1[head[i]].append(row[i])

        cwd = os.path.dirname(os.path.realpath(__file__))
        currentDay = datetime.now().day
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        currentSecond = datetime.now().second
        currentMinute = datetime.now().minute
        currentHour = datetime.now().hour
        file_name = f"out_{currentDay}_{currentMonth}_{currentYear}_{currentHour}{currentMinute}{currentSecond}.csv"
        file_absolute_path = os.path.join(cwd, 'output', file_name)
        with open(file_absolute_path, "w", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(list1)
        chrome.close()
        total_download = convert_to_gb(dict1['Download'])
        total_upload = convert_to_gb(dict1['Upload'])

        print(f"Total Download Usage: {total_download:.2f}")
        print(f"Total Upload Usage: {total_upload:.2f}")
        print(f"Wiretel Data Usage : {(total_download + total_upload):.2f} GB")
        content = f"""
        Total Download Usage: {total_download:.2f} GB
        Total Upload Usage: {total_upload:.2f} GB
        """
        to_emails = config.RECIPIENT_EMAIL
        my_email = config.SENDER_EMAIL

        subject = f"Wiretel Data Usage : {(total_download + total_upload):.2f} GB"
        send_mail(my_email, to_emails, subject, content, file_absolute_path, file_name)

    except InvalidTagForAuthorError as e:
        print(e)
    except Exception as e:
        print(e)
