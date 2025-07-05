from master import MasterConfiguration
from booking import Booking
from checkin import CheckIn
from checkout import Checkout

class Main:

    def __init__(self):
        self.master = MasterConfiguration()
        self.booking = Booking()
        self.checkin = CheckIn()
        self.checkout = Checkout()
    
    def run(self):
        while True:
            print("\n Main Menu:")
            print("1. Master Configuration")
            print("2. Booking Menu (Advance/Cancel)")
            print("3. Direct Check-In")
            print("4. Checkout")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ") 

            if choice == "1":
                self.master.run()
            elif choice == "2":
                self.booking.run()
            elif choice == "3":
                self.checkin.run()
            elif choice == "4":
                try:
                    booking_id = int(input("Enter booking ID to checkout: "))
                    self.checkout.checkout(booking_id)
                except ValueError:
                    print("\u274c Invalid booking ID.")
            elif choice == "5":
                print("Exiting program.")
                break
            else:
                print("Invalid choice") 

if __name__ == "__main__":
    main = Main()
    main.run()
