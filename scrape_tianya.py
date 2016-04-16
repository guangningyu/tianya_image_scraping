#!/usr/bin/python

import os
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def scrape_page_images(base_url, page_num, output_dir, img_black_list):

    print '> Dealing with page %d...' % page_num

    page_url = base_url.format(str(page_num))
    soup = BeautifulSoup(requests.get(page_url).text, "lxml")
    img_list = []
    img_num = 0
    for img in soup.findAll('img'):
        try:
            img_url = img['original']
            if img_url not in img_black_list:
                img_num += 1
                img_list.append((page_num, img_num, img_url))
        except Exception as e:
            continue

    for page_num, img_num, img_url in img_list:
        img_path = get_img_path(page_num, img_num, img_url, output_dir)
        save_image(page_url, img_url, img_path)


def get_img_path(page_num, img_num, img_url, output_dir):
    img_type = img_url.strip().split('.')[-1]
    img_nm = str('%04d' % page_num) + '_' + str('%02d' % img_num) + '.' + img_type
    return output_dir + '/' + img_nm


def save_image(page_url, img_url, img_path):
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)rome/41.0.2272.101 Safari/537.36',
        'Referer':'%s' % page_url
    }
    img_content = requests.get(img_url, stream=True, headers=header).content
    try:
        with open(img_path, 'wb') as img:
            img.write(img_content)
            return
    except Exception as e:
        print '%s cannot be saved.' % img_path
        return


if __name__ == '__main__':

    # the url of the article, with the page number as a parameter
    base_url = 'http://bbs.tianya.cn/post-worldlook-223829-{0}.shtml#ty_vip_look[%E9%84%99%E8%A7%86%E6%8A%A2%E6%B2%99%E5%8F%91%E7%9A%84]'

    # create the folder to save the images
    output_dir = os.getcwd() + '/' + 'images'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # if any image is not expected to be saved, put it here
    img_black_list = []

    # the number of pages of the article
    max_page_num = 1000

    for i in range(max_page_num):
        page_num = i + 1
        scrape_page_images(base_url, page_num, output_dir, img_black_list)

