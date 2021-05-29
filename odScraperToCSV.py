# -*- coding: utf-8 -*-

import requests
import bs4
import re
import csv

#print(odResultsCountInt)

odLibraries = open('odLibraries.csv')
odLibrariesOutput = open('odLibrariesOutput.csv', 'w', newline="")

def main():
    csvReader = csv.DictReader(odLibraries)
    csvWriter = csv.DictWriter(odLibrariesOutput, ['odCatalogue',
                                                   'url',
                                                   'totalCollection',
                                                   'totalEbooks',
                                                   'totalEbookFiction',
                                                   'totalEbookNonFiction',
                                                   'totalAudiobooks',
                                                   'totalAudiobookFiction',
                                                   'totalAudiobookNonFiction'])
    csvWriter.writeheader()
    for row in csvReader:
        try:
            totalCollection = requests.get(row['url']+'search/title')
            totalEbooks = requests.get(row['url']+'search/title?mediaType=ebook')
            totalEbookFiction = requests.get(row['url']+'search/title?mediaType=ebook&subject=26')
            totalEbookNonFiction = requests.get(row['url']+'search/title?mediaType=ebook&subject=111')
            totalAudiobooks = requests.get(row['url']+'search/title?mediaType=audiobook')
            totalAudiobookFiction = requests.get(row['url']+'search/title?mediaType=ebook&subject=26')
            totalAudiobookNonFiction = requests.get(row['url']+'search/title?mediaType=ebook&subject=111')
            print("Processing Library: ", row['odCatalogue'])
            csvWriter.writerow({'odCatalogue': row['odCatalogue'],
                       'url': row['url'],
                       'totalCollection': extractCount(totalCollection),
                       'totalEbooks': extractCount(totalEbooks),
                       'totalEbookFiction': extractCount(totalEbookFiction),
                       'totalEbookNonFiction': extractCount(totalEbookNonFiction),
                       'totalAudiobooks': extractCount(totalAudiobooks),
                       'totalAudiobookFiction': extractCount(totalAudiobookFiction),
                       'totalAudiobookNonFiction': extractCount(totalAudiobookNonFiction)})
        except Exception as err:
            print("An error occured while processing library: ", row['odCatalogue'])
            print(err)
            continue
        

        
def extractCount(slug):
    soup = bs4.BeautifulSoup(slug.text, 'html.parser')
    odResults = soup.select('.search-text')[0].get_text()
    odResultsCount = re.search('(?<= of )(.*)(?= results)',odResults).group()
    odResultsCountInt = int(odResultsCount.replace(",",""))
    return(odResultsCountInt)

main()
odLibrariesOutput.close