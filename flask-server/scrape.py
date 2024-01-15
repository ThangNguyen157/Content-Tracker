import bs4
import requests

class Scrape:
    def __init__(self, url):
        self.url = url
    def scrape(self):
        splash_url = 'http://localhost:8050/render.html'

        params = {
        'url': self.url,
        'wait': 2,  # Time to wait for JavaScript to execute (adjust as needed)
        'render_all': 1,
        }
        
        try:
            data = requests.get(splash_url, params = params)
            data.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            # Handle the error, which might include DNS resolution issues
            return "DNS address could not be found"
        if data.status_code < 200 or data.status_code >= 300:
            return data.status_code
        soup = bs4.BeautifulSoup(data.text, "html.parser")
        return soup
    
    def getModifiedHTMLCSS(self, soup):
        imgs = soup.find_all('img')
        for img in imgs:
            img['src'] = 'placeholer.png'
        
        aTags = soup.find_all('a')
        for index, aTag in enumerate(aTags):
            del aTag['href']
        
        style = soup.find_all('style')
        styleTag = ''.join(str(tag) for tag in style)
        
        css = soup.find_all('link', rel='stylesheet')
        cssTag = ''.join(str(tag) for tag in css)
        '''for tag in css:
            cont = requests.get(tag['href'])
            cssContent += cont.text'''
        text = []
        indeces = []
        #content = list(html.find_all(string=True))
        content = list(soup.descendants)

        #filter to get only the text in the content list
        for index, value in enumerate(content):
            if type(value) == bs4.element.NavigableString and not value.isspace():
                '''while '\n' in value:
                    value = value.replace('\n', "")
                text.append(value)'''
                #indeces.append(index)
                value.wrap(soup.new_tag("span"))
                value.parent['id'] = str(index)
                #this.id return the id of the tag that the function is inside the onclick of
                value.parent['onclick'] = "changeColor(this.id)"
                value.parent['class'] = "change"
                
        newTag = soup.new_tag('script', src='viewpage.js')
        soup.head.append(newTag)

        newTag = soup.new_tag('style')
        newTag.string = '.change:hover { background-color: #ffff80; color: black}'
        soup.head.append(newTag)
        return str(soup.prettify())
'''
d = Scrape('https://www.ebay.com/itm/204274527497?var=504836709828&_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20230823115209%26meid%3Dacd787ba9434468db0ee2d96a67ecfe6%26pid%3D101800%26rk%3D1%26rkt%3D1%26sd%3D204274527497%26itm%3D504836709828%26pmt%3D1%26noa%3D1%26pg%3D4375194%26algv%3DRecentlyViewedItemsV2SignedOut%26brand%3DBrand&_trksid=p4375194.c101800.m5481&_trkparms=parentrq%3Ad6dd115518c0ab8e1eac1286ffff66ba%7Cpageci%3A2f056412-ab5b-11ee-8541-92c4b5d57a12%7Ciid%3A1%7Cvlpname%3Avlp_homepage', 10, 'koio')

a = d.scrape()
print(a)
b = d.getModifiedHTMLCSS(a)
print(b)'''
