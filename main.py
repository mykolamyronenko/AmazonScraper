from requests_html import HTMLSession
import pandas as pd
import time

def get_amazon_data(search_query, max_pages=5):
    session = HTMLSession()
    search = search_query.replace(' ', '+').lower()
    base_url = 'https://www.amazon.com/'
    headers = {
        'Accept-Language': 'en,en-US;q=0.7,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Fire~fox/130.0'
    }
    
    titles, prices, links = [], [], []
    
    for page in range(1, max_pages + 1):
        url = f'https://www.amazon.com/s?k={search}&page={page}'
        
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching data from page {page}: {e}")
            break
        
        container = response.html.xpath('//div[@data-component-type="s-search-result"]')
        
        if not container:
            print(f"No more results found on page {page}.")
            break
        
        for element in container:
            if element.xpath('.//div[@class="a-row a-spacing-micro"]'):
                continue
            
            title = element.xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]', first=True)
            titles.append(title.text if title else None)
            
            price = element.xpath('.//span[@class="a-offscreen"]', first=True)
            prices.append(price.text if price else None)
            
            link = element.xpath('.//a[@class="a-link-normal s-no-outline"]', first=True)
            links.append(base_url + link.attrs['href'] if link else None)
        
        time.sleep(2)
    
    session.close()
    
    data = {'Title': titles, 'Price': prices, 'Link': links}
    df = pd.DataFrame(data)
    print(df)
    
    filename = search_query.replace(' ', '_').lower()
    df.to_excel(f'{filename}.xlsx', index=False)

if __name__ == "__main__":
    search_query = input('What do you want to scrape?').strip()
    get_amazon_data(search_query)
