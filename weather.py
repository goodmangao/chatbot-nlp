# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag

def weather():
    print('BOT:Welcome to weather search')
    print('BOT:Which city do you want to search?')
    text = input('')
    tokens = word_tokenize(text)
    post = pos_tag(tokens)
    address = ''
    # Find place name information from sentences
    for n in range(len(post)):
        if post[n][1] == 'NNP':
            address = post[n][0]
    if address == '':
        for n in range(len(post)):
            if post[n][1] == 'NN':
                address = post[n][0]
    print('BOT:Which day do you want to search,today or tomorrow?')  # Select the date to be queried
    reply = input('')
    if 'today' in reply:
        url = 'https://www.meteoprog.co.uk/en/weather/{my_address}/'.format(my_address=address)
        print('BOT:Searching, please wait')
        # today
        try:
            r = requests.get(url)  # Use requests to grab web page information
            r.raise_for_status()   # It can stop the program when an exception occurs in the program
            r.encoding = r.apparent_encoding
            html = r.text
        except:
            print('error')

        final_list = []
        soup = BeautifulSoup(html, 'html.parser')  # Parse web pages with BeautifulSoup
        body = soup.body
        data = body.find('div', {'class': "page-columns-wrapper"})    # Find the crawl range

        weather_list = []

        celsius = data.find('span', {'class': "feels-like"})  # find temperature
        celsius1 = celsius.find_all('b')
        weather_list.append(celsius1[0].string)
        weather1 = data.find('h3').string     # find weather
        weather_list.append(weather1)

        final_list.append(weather_list)  # Add the weather_list list to the final_list list
        num = 1
        for i in range(num):
            final = final_list[i]
            print("BOT:Today is {:^1}.\t{:^1}\t".format(final[0], final[1]))   # Output crawl results

    # tomorrow
    if 'tomorrow' in reply:
        date = 'tomorrow'
        url = 'https://www.meteoprog.co.uk/en/weather/{my_address}/{my_date}/'.format(my_address=address, my_date=date)
        print('BOT:Searching, please wait')
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
        except:
            print('error')

        final_list = []
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.body
        data = body.find('div', {'class': "page-columns-wrapper"})

        weather_list = []

        celsius = data.find('span', {'class': "feels-like"})
        celsius1 = celsius.find_all('b')
        weather_list.append(celsius1[0].string)
        weather1 = data.find('h3').string
        weather_list.append(weather1)

        final_list.append(weather_list)
        num = 1
        for i in range(num):
            final = final_list[i]
            print("BOT:Tomorrow is {:^1}.\t{:^1}\t".format(final[0], final[1]))

# weather()