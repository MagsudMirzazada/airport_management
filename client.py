import requests
from termcolor import colored

BASE = 'http://127.0.0.1:5000/'

token_ = None
#s
class User:
    def __init__(self):
        # self.token = None
        self.usrname = None
        self.password = None

    def get(self):
        source = input(colored('Please, enter source city: ', 'green'))
        destination = input(colored('Please, enter destination city: ', 'green'))
        link = f"{BASE}/flights/{source}/{destination}"
        res = requests.get(link)
        print(res.json())
        return res
        
    def post(self):
        from_city = input(colored("From: ", 'green'))
        to_city = input(colored("To: ", 'green'))
        departure_time = input(colored("Departure time: ", 'green'))
        arrival_time = input(colored("Arrival time: ", 'green'))
        airplane_info = input(colored("Airplane info: ", 'green'))
        passengers_count = input(colored("Number of passengers: ", 'green'))
        data={
            "from_city": from_city if from_city else None,
            "to_city": to_city if to_city else None,
            "departure_time": departure_time if departure_time else None,
            "arrival_time": arrival_time if arrival_time else None,
            "airplane_info": airplane_info if airplane_info else None,
            "passengers_count": int(passengers_count) if passengers_count else None,
            "token": token_
        }
        res = requests.post(f"{BASE}/flights", data=data)
        return res
    
    def put(self):
        flight_id = input(colored('Flight ID: ', 'green'))
        from_city = input(colored("From: ", 'green'))
        to_city = input(colored("To: ", 'green'))
        departure_time = input(colored("Departure time: ", 'green'))
        arrival_time = input(colored("Arrival time: ", 'green'))
        airplane_info = input(colored("Airplane info: ", 'green'))
        passengers_count = input(colored("Number of passengers: ", 'green'))
        data = {
            "flight_id": flight_id if flight_id else None,
            "from_city": from_city if from_city else None,
            "to_city": to_city if to_city else None,
            "departure_time": departure_time if departure_time else None,
            "arrival_time": arrival_time if arrival_time else None,
            "airplane_info": airplane_info if airplane_info else None,
            "passengers_count": int(passengers_count) if passengers_count else None,
            "token": token_
        }
        res = requests.put(f"{BASE}/flights", data=data)
        return res

    def delete(self):
        flight_id = int(input(colored("Flight id: ", 'green')))
        data = {
            "flight_id": flight_id,
            "token": token_
        }
        res = requests.delete(f"{BASE}/flights", data=data)
        return res

    def login(self):
        self.username = input('Admin Username: ')
        self.password = input('Admin password: ')
        token = requests.post(BASE + '/authentication_authorization',
                    {'username': self.username, 'password': self.password})
        # print(token.json()['token'])
        global token_
        token_ = token.json()['token']
        # print(colored(f"{self.token}", 'red'))
        return token

    def end_session(self):
        global token_
        data = {"token": token_}
        res = requests.post(f"{BASE}/end_session", data=data)
        token_ = None
        print(colored(res.json()['message'], 'yellow'))
        return res

def homepage():
    while True:
        user = User()
        print('='*60)
        print('''
        Welcome to Airline Information Center
        -------------------------------------
        1. Login
        2. Show my token
        3. Get flights info
        4. Manipulate flights
        5. Logout
        6. Exit''')
        print('='*60)
        operation = str(input(colored('Please, enter service number: ', 'green')))
        if operation == '1':
            user.login()
            user.token = token_
        elif operation == '2':
            print(colored(token_, 'yellow'))
        elif operation == '3':
            user.get()
        elif operation == '4':
            print('='*60)
            print('''
            ===Welcome to Admin Panel===
            1. Add flight
            2. Update flight
            3. Delete flight''')
            command = input(colored('Hi admin, please enter command number: ', 'green'))
            if command == '1':
                user.post()
            elif command == '2':
                user.put()
            elif command == '3':
                user.delete()
            else:
                print(colored('Invalid command number!', 'red'))
        elif operation == '5':
            user.end_session()
        elif operation == '6':
            break
        else:
            print(colored('Please enter valid number...', 'red'))



def main():
    homepage()

if __name__ == '__main__':
    main()