import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
from pprint import pprint
import csv


url = 'https://finance.yahoo.com/quote/'


def get_input(url):
    symbols = pd.read_csv('Input.csv')
    symbols = symbols['Symbols'].tolist()

    list_of_urls = []
    for i in range(0, len(symbols)):
        final_url = url + symbols[i] + '?p=' + symbols[i]
        list_of_urls.append(final_url)
    return list_of_urls


def load_needed_data(url):
    head = ['Ticker','Previous Close','Market Cap','Open','Beta(5Y Monthly', 'Bid',
            'PE Ratio', 'Ask', 'EPS','Day\'s Range','Earnings Date','52 Week Range','Forward Dividend',
            'Volume','Ex-Dividend Date','Avg Volume','1y Target Estimate']
    head = pd.DataFrame(head).transpose()
    head.to_csv('Data.csv', index=False, header= False)

    for k in range(0, len(url)):
        page = requests.get(url[k])

        soup = BeautifulSoup(page.content, "lxml")

        a = soup.find('div', class_= 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)')
        ns = a.find('h1', class_= 'D(ib) Fz(18px)').text.split('(')
        attribute0 = []
        name = ns[0]
        symbol = ns[1].replace(')', '')
        attribute0.append(symbol)
        attribute0.append(name)


        b = soup.find('div', class_= 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')
        left_table = b.findAll('tr', class_='Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)')

        attribute1 = []
        for i in range(0, len(left_table)):
            info1 = left_table[i].find('td', class_='Ta(end) Fw(600) Lh(14px)').text
            attribute1.append(info1)


        c =  soup.find('div', class_= "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)")
        right_table = c.findAll('tr', class_='Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)')

        attribute2 = []
        for i in range(0, len(right_table)):
            info2 = right_table[i].find('td', class_='Ta(end) Fw(600) Lh(14px)').text
            attribute2.append(info2)

        pd_attr0 = pd.Series(attribute0)
        pd_attr1 = pd.Series(attribute1)
        pd_attr2 = pd.Series(attribute2)
        tot_attr = pd.concat([pd_attr0, pd_attr1, pd_attr2])
        df = pd.DataFrame(tot_attr)
        result = df.transpose()
        result = result.rename_axis(None)

        with open('Data.csv', 'a') as f:
            result.to_csv(f, index= False, header= False)
            print('Loading...')
    print('The data is successfully loaded onto the file!')


if __name__ == "__main__":
    list_res = get_input(url)
    load_needed_data(list_res)