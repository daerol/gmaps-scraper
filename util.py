import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import concurrent.futures


# Add a another column named domain_new, contains domains with http://
def get_url(df):
    df['domain_new'] = np.where(df['Website'].notna(), 'http://' + df['Website'], df['Website'])
    df['domain_new'] = df['domain_new'].str.strip()  # get rid of blank space after
    urllist = list(df['domain_new'])
    return urllist


# Method used to obtain Facebook links for all companies in data frame.
def get_fb(data):
    print('Starting fb data')
    fb_list = []

    # Used to search for a Facebook link on company website. Will apply link to Facebook column.
    # Otherwise will add an empty cell to Facebook column.
    try:
        req = requests.get(data, headers)
        soup = BeautifulSoup(req.content, 'lxml')
        fb = soup.find('a', {'href': re.compile("https?://(www\\.)?facebook\\.com/[^(share)]?(\\w+\\.?)+")})
        fb_link = fb['href']
        fb_list.append(fb_link)
    except(ConnectionError, Exception):
        fb_link = ''
        fb_list.append(fb_link)
    print('Finished fb data')
    return fb_list


# Method used to obtain Instagram links for all companies in data frame.
def get_instagram(data):
    print('Starting instagram data')
    ins_list = []

    # Used to search for a Instagram link on company website. Will apply link to Instagram column.
    # Otherwise will add an empty cell to Instagram column.
    try:
        req = requests.get(data, headers)
        soup = BeautifulSoup(req.content, 'lxml')
        ins = soup.find('a', {'href': re.compile("https?://(www\\.)?instagram\\.com/[^(share)]?(\\w+\\.?)+")})
        ins_link = ins['href']
        ins_list.append(ins_link)
    except(ConnectionError, Exception):
        ins_link = ''
        ins_list.append(ins_link)
    print('Finished instagram data')
    return ins_list


# Method used to obtain Twitter links for all companies in data frame.
def get_twitter(data):
    print('Starting twitter data')
    twitter_list = []

    # Used to search for a Twitter link on company website. Will apply link to Twitter column.
    # Otherwise will add an empty cell to Twitter column.
    try:
        req = requests.get(data, headers)
        soup = BeautifulSoup(req.content, 'lxml')
        twt = soup.find('a', {'href': re.compile("https?://(www\\.)?twitter\\.com/[^(share)]?(\\w+\\.?)+")})
        twt_link = twt['href']
        twitter_list.append(twt_link)
    except(ConnectionError, Exception):
        twt_link = ''
        twitter_list.append(twt_link)
    print('Finished twitter data')
    return twitter_list


# Method used to obtain Facebook Pixel info for all companies in data frame.
def facebook_pixel(data):
    print('Starting fp_list data')
    fp_list = []
    text_str = 'Facebook Pixel Code'

    # Used to search for a Facebook Pixel info. Will yes to Facebook Pixel column if found and no otherwise.
    try:
        result = requests.get(data, headers)
        fb_text = result.content.decode()
        res = re.search(text_str, fb_text)
        if res:
            fp_data = 'Yes'
        else:
            fp_data = 'No'
        fp_list.append(fp_data)
    except(ConnectionError, Exception):
        fp_data = 'No'
        fp_list.append(fp_data)
    print('Finished fb_list data')
    return fp_list


# Method used to obtain Google Analytics info for all companies in data frame.
def google_analytics(data):
    print('Starting ga_list data')
    ga_list = []
    ga_str = 'google-analytics.com'

    # Used to search for a Google Analytics info. Will yes to Google Analytics column if found and no otherwise.
    try:
        result = requests.get(data, headers=headers)
        ga_text = result.content.decode()
        res = re.search(ga_str, ga_text)
        if res:
            ga_data = 'Yes'
        else:
            ga_data = 'No'
        ga_list.append(ga_data)
    except(ConnectionError, Exception):
        ga_data = 'No'
        ga_list.append(ga_data)
    print('Finished ga_list data')
    return ga_list


# Method used to obtain Google Tag info for all companies in data frame.
def google_tag(data):
    print('Starting gt_list data')
    gt_list = []
    gt_str = 'Google Tag Manager|gtm|Globle site tage|gtag'

    # Used to search for a Google Tag info. Will yes to Google Tag column if found and no otherwise.
    try:
        result = requests.get(data, headers=headers)
        gt_text = result.content.decode()
        res = re.search(gt_str, gt_text)
        if res:
            gt_data = 'Yes'
        else:
            gt_data = 'No'
        gt_list.append(gt_data)
    except(ConnectionError, Exception):
        gt_data = 'No'
        gt_list.append(gt_data)
    print('Finished gt_list data')
    return gt_list


# A call that starts the addition link process through an object method.
def get_all_links(companyInfo) -> object:
    wb = openpyxl.Workbook()
    wb.save('ScrapedData/' + companyInfo + '.xlsx')

    print("Getting additional links for companies")
    # upload file to colab "files"
    df = pd.read_excel('ScrapedData/' + companyInfo + '-tmp2.xlsx')
    df.index = np.arange(1, len(df) + 1)

    # Creating http urls from website column for click-able access.
    urllist = get_url(df)

    # Start multi threading code for each addition link and column added.
    # Map added to assure the data stays in the same order as file and not in the order of being processed.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fb_col = executor.map(get_fb, urllist)
        ins_col = executor.map(get_instagram, urllist)
        twt_col = executor.map(get_twitter, urllist)
        fb_pixel = executor.map(facebook_pixel, urllist)
        ga_col = executor.map(google_analytics, urllist)
        gtag_col = executor.map(google_tag, urllist)

    # Adding all the new data to their columns in the data frame.
    df['facebook_url'] = np.array(list(fb_col))
    df['instagram_url'] = np.array(list(ins_col))
    df['twitter_url'] = np.array(list(twt_col))
    df['facebook_pixel'] = np.array(list(fb_pixel))
    df['google_analytics'] = np.array(list(ga_col))
    df['google_tag_manager'] = np.array(list(gtag_col))

    #  Deleting the http click-able column as it is no longer needed.
    del df['domain_new']