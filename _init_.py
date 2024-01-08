import bs4
import requests
from lxml import etree

def getInput():
    url = input("Enter url of the page: ");
    while True:
        try:
            time_interval = int(input("How often do want the website to be checked(in minutes)?(At least every 10 mins): "))        
            if time_interval >= 10:
                break
            else:
                print("Must be at least every 10 mins.")
        except ValueError:
            print("Invalid input. Try again.")
    return url, time_interval

def scraping(url):
    splash_url = 'http://localhost:8050/render.html'

    params = {
    'url': url,
    'wait': 2,  # Time to wait for JavaScript to execute (adjust as needed)
    'render_all': 1,
    }
    data = requests.get(splash_url, params = params)

    soup = bs4.BeautifulSoup(data.text, "html.parser")
    return soup, data

def getinput2(length):
    while True:
        try:
            number = int(input("Enter the number associates the text you want to check: "))
            if number < length and number > 0:
                break
            else:
                print("The number should be between range 0-"+str(length)+".")
        except ValueError:
            print("Invalid input. Try again")
    return number

def main():
    url, timeInterval = getInput()
    html, data = scraping(url)
    
    text = []
    indeces = []
    content = list(html.descendants)

    #filter to get only the text in the content list
    for index, value in enumerate(content):
        if type(value) == bs4.element.NavigableString and not value.isspace():
            while '\n' in value:
                value = value.replace('\n', "")
            text.append(value)
            indeces.append(index)
    
    for index, value in enumerate(text):
        print(str(index+1) + ". " + value)

    number = getinput2(len(text))
    
    #print (content[indeces[number-1]-1].parent.contents)
    

if __name__ == "__main__":
    main()