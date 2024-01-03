from bs4 import BeautifulSoup as bs
import requests
def get_input():
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



def main():
    url, time_interval = get_input()
    splash_url = 'http://localhost:8050/render.html'

    params = {
    'url': url,
    'wait': 5,  # Time to wait for JavaScript to execute (adjust as needed)
    'render_all': 1,
    }
    data = requests.get(splash_url, params = params)

    soup = bs(data.text, "html.parser")
    print(soup.prettify())

if __name__ == "__main__":
    main()