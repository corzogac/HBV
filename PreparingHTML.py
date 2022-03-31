from bs4 import BeautifulSoup

soup = BeautifulSoup()
body = soup.new_tag('body')
soup.insert(0, body)
table = soup.new_tag('table')
body.insert(0, table)

with open('info.txt') as infile:
    for line in infile:
        row = soup.new_tag('tr')
        col1, col2 = line.split("->")
        for coltext in (col2, col1): # important that you reverse order
            col = soup.new_tag('td')
            col.string = coltext
            row.insert(0, col)
        table.insert(len(table.contents), row)

with open('file.html', 'w') as outfile:
    outfile.write(soup.prettify())