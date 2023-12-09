from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.express as px

url = 'http://quotes.toscrape.com'
# Request in case of 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# Lists and dictionaries to collect data
all_quotes = []
author_data = {}
tag_data = {}

# Scraping quotes from the first 10 pages
for page_num in range(1, 11):
    page_url = f'{url}/page/{page_num}'
    req = Request(page_url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        
        # Author Statistics
        author_data[author] = author_data.get(author, 0) + 1
        
        # Quote Analysis
        all_quotes.append(text)
        
        # Tag Analysis
        for tag in tags:
            tag_data[tag] = tag_data.get(tag, 0) + 1

# Author with the most and least quotes
most_quotes_author = max(author_data, key=author_data.get)
least_quotes_author = min(author_data, key=author_data.get)

# Quote Analysis
average_quote_length = sum(len(quote) for quote in all_quotes) // len(all_quotes)
longest_quote = max(all_quotes, key=len)
shortest_quote = min(all_quotes, key=len)

# Tag Analysis
most_popular_tag = max(tag_data, key=tag_data.get)
total_tags_used = sum(tag_data.values())

# Visualization - Top 10 Authors
top_authors_df = sorted(author_data.items(), key=lambda x: x[1], reverse=True)[:10]
top_authors_names, top_authors_quotes = zip(*top_authors_df)
fig_authors = px.bar(x=top_authors_names, y=top_authors_quotes, title='Top 10 Authors and Number of Quotes')

# Visualization - Top 10 Tags
top_tags_df = sorted(tag_data.items(), key=lambda x: x[1], reverse=True)[:10]
top_tags_names, top_tags_count = zip(*top_tags_df)
fig_tags = px.bar(x=top_tags_names, y=top_tags_count, title='Top 10 Tags and Popularity')

# Displaying results
print()
print("Author Statistics ------------------------------")
for author, count in author_data.items():
    print(f"{author}: {count}")

print("\nAuthor with the most quotes ")
print(f"{most_quotes_author}: {author_data[most_quotes_author]} quotes")

print("\nAuthor with the least quotes ")
print(f"{least_quotes_author}: {author_data[least_quotes_author]} quotes")

print("\nQuote Analysis --------------------------------")
print(f"Average Length of Quotes: {average_quote_length} characters")
print(f"Longest Quote: {longest_quote}")
print()
print(f"Shortest Quote: {shortest_quote}")

print("\nTag Analysis ----------------------------------")
print(f"Most Popular Tag: {most_popular_tag}")
print(f"Total Tags Used: {total_tags_used}")

# Displaying visualizations ---------------------------------------------------
fig_authors.show()
fig_tags.show()
