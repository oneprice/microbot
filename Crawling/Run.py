from Crawling.Crawl import Crawl
import time


def main():

    obj = Crawl('5639964597')
    obj.main()

    F_json = {'api': 'item_detail', 'data': obj.data_list}




if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

