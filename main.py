import requests
from bs4 import BeautifulSoup

url = 'https://www.timeanddate.com/holidays/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#find table containing holidays
table = soup.find('table', {'class': 'table--holindex'})

holidays = []

#iterate  each row in table body
for row in table.tbody.find_all('tr'):
    cells = row.find_all(['th', 'td'])
    cell_text = [cell.get_text(strip=True) for cell in cells]

    if cells[0].name == 'th':
        #new date row
        date = cell_text[0]
        day = cell_text[1]
        name = cell_text[2]
        where = cell_text[3]
    elif cells[0].has_attr('colspan') and cells[0]['colspan'] == '2':
        #continue row with empty first cell
        date = holidays[-1]['date']
        day = holidays[-1]['day']
        name = cell_text[1]
        where = cell_text[2]
    else:
        #handle any other cases if necessary
        date = holidays[-1]['date']
        day = holidays[-1]['day']
        name = cell_text[0]
        where = cell_text[1]

    #some holidays may span multiple countries
    countries = [country.strip() for country in where.split(',')]

    holidays.append({
        'date': date,
        'day': day,
        'name': name,
        'countries': countries
    })

#get input country from the user
input_country = input("Enter a country: ").strip().lower()

#search for holidays in  input country
found = False
print(f"Holidays in {input_country.title()} in the next 7 days:")
for holiday in holidays:
    #check if the input country is in the list of countries for the holiday
    if any(input_country == country.lower() for country in holiday['countries']):
        print(f"{holiday['date']} ({holiday['day']}): {holiday['name']}")
        found = True

if not found:
    print(f"No holidays found for {input_country.title()} in the next 7 days.")
