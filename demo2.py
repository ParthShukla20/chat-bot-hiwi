from bs4 import BeautifulSoup

html_code = '''
... [Your HTML Code]
'''

soup = BeautifulSoup(html_code, 'html.parser')

universities_div = soup.find('div', class_='choices__list--dropdown')

# Extract the list of universities
universities_list = [item['data-value'] for item in universities_div.find_all('div', class_='choices__item--selectable')]

# Print the list of universities
print(universities_list)
