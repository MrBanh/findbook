#! python3
# findbook.py - Launches browser, navigates to Library Genesis, and searches for a book
# using the command line or clipboard. Open the first 3 links that has pdf extensions

import webbrowser as wb
import requests as req
import pyperclip as pc
import bs4
import sys


def findBook(book):
    print(f'Searching for {book}...')
    res = req.get(f'http://gen.lib.rus.ec/search.php?req={book}')

    # Checks if request is successful. If not, stop program and raise exception
    res.raise_for_status()

    # Opens browser to the search results
    wb.open(f'http://gen.lib.rus.ec/search.php?req={book}')

    # Parses the HTML obtained from the requests module
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    linkElems = soup.select(
        'tr[valign="top"] td[width="500"] a')  # Select each link
    extElems = soup.select('tr[valign="top"] td[nowrap]')
    pdfLinks = []

    # Find the rows that has 'pdf' as the extension and append the link to a list
    for i in range(len(extElems)):
        if str(extElems[i].getText()) == 'pdf':
            pdfLinks.append(linkElems[int(i / 3)].get('href'))

    # Determine number of tabs to open for each pdf link
    numOpen = min(1, len(pdfLinks))
    for i in range(numOpen):
        url = 'http://gen.lib.rus.ec/' + pdfLinks[i]
        wb.open(url)

        toDownload = input(f'Download from {url}? (y/n): ')
        if toDownload.lower() == 'y':
            # Downloads the web page from the pdf link
            pdfRes = req.get(url)
            pdfRes.raise_for_status()
            # Parse the page of the pdf link
            pdfSoup = bs4.BeautifulSoup(pdfRes.text, features="lxml")
            # Choose the first mirror
            mirrorLink = pdfSoup.select('tr td a[title="Gen.lib.rus.ec"]')

            # Downloads the web page of the first mirror download link
            mirrorRes = req.get(mirrorLink[0].get('href'))
            mirrorRes.raise_for_status()
            mirrorSoup = bs4.BeautifulSoup(mirrorRes.text, features="lxml")
            dlLink = 'http://93.174.95.29' + mirrorSoup.select('tr #info h2 a')[0].get('href')

            # Downloads the file to computer
            print(f'Downloading from {dlLink}...')
            wb.open(dlLink)

    print('\nDone!\n')


if len(sys.argv) > 1:
    # Get the book title or ISBN from command line
    book = ' '.join(sys.argv[1:])
    findBook(book)
else:
    # Get the book title or ISBN from clipboard
    book = pc.paste()
    findBook(book)
