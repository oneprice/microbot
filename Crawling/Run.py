from Crawl import Crawl
from selenium import webdriver
from pyvirtualdisplay import Display
from datetime import datetime


def main():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    now = datetime.now()

    print('start' + str(now))
    obj = Crawl('5639964597', display, driver)
    obj.main()
    now = datetime.now()

    F_json = {'time': now, 'api': 'item_detail', 'data': obj.data_list}
    print('End'+ str(now))


if __name__ == '__main__':
    main()
