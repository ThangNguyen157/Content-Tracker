def get_input():
    url = input("Enter url of the page: ");
    while True:
        try:
            time_interval = int(input("How often do want the website to be checked(in minutes)?(At least every 10 mins): "))        
            if time_interval >= 10:
                break;
            else:
                print("Must be at least every 10 mins.")
        except ValueError:
            print("Invalid input. try again.")

def main():
    get_input()

if __name__ == "__main__":
    main()