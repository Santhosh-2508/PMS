import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Booking:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='santho25.08',  
                database='hoteldesk_management_system'
            )
            self.cursor = self.conn.cursor()
            self.create_table()
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                booking_type VARCHAR(255) NOT NULL,
                roomid INT NOT NULL,
                customer_name VARCHAR(255) NOT NULL,
                customer_phone VARCHAR(255) NOT NULL,
                customer_email VARCHAR(255) NOT NULL,
                customer_address VARCHAR(255) NOT NULL,
                customer_city VARCHAR(255) NOT NULL,
                customer_state VARCHAR(255) NOT NULL,
                customer_gender VARCHAR(255) NOT NULL,
                checkin_datetime datetime NOT NULL,
                checkout_datetime datetime NOT NULL,
                booking_datetime datetime NOT NULL,
                payadvance INT NOT NULL,
                tariff INT,
                tariff_tax INT,
                checked_out INT DEFAULT 0,
                FOREIGN KEY (roomid) REFERENCES rooms(roomid)
            )
        ''')
        self.conn.commit()

    def is_valid_room(self, roomid):
        self.cursor.execute('SELECT roomid FROM rooms WHERE roomid = %s', (roomid,))
        return self.cursor.fetchone() is not None

    def get_tariff_and_tax(self, roomid):
        self.cursor.execute('SELECT tariff, tariff_tax FROM rooms WHERE roomid = %s', (roomid,))
        return self.cursor.fetchone()

    def get_customer_details(self):
        customer_name = input("Enter customer name: ")
        customer_phone = input("Enter customer phone: ")
        customer_email = input("Enter customer email: ")
        customer_address = input("Enter customer address: ")
        customer_city = input("Enter customer city: ")
        customer_state = input("Enter customer state: ")
        customer_gender = input("Enter customer gender: ")
        return (customer_name, customer_phone, customer_email, customer_address,
                customer_city, customer_state, customer_gender)

    def advance_room_booking(self, roomid, *details):
        if not self.is_valid_room(roomid):
            print(f"❌ Room ID {roomid} does not exist.")
            return
        tariff_info = self.get_tariff_and_tax(roomid)
        if not tariff_info:
            print(f"❌ No tariff info for room ID {roomid}.")
            return
        tariff, tariff_tax = tariff_info
        print(f"Room Tariff: {tariff}, Tax: {tariff_tax}")
        try:
            payadvance = int(input("Enter advance amount to pay: "))
            if payadvance <= 0:
                print("❌ Advance payment required.")
                return
        except ValueError:
            print("❌ Invalid advance amount.")
            return
        checkin = input("Enter check-in datetime (YYYY-MM-DD HH:MM:SS): ")
        checkout = input("Enter check-out datetime (YYYY-MM-DD HH:MM:SS): ")
        booking_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO bookings (
                booking_type, roomid, customer_name, customer_phone, customer_email,
                customer_address, customer_city, customer_state, customer_gender,
                checkin_datetime, checkout_datetime, booking_datetime, payadvance, tariff, tariff_tax
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', ("advance", roomid, *details, checkin, checkout, booking_datetime, payadvance, tariff, tariff_tax))
        self.conn.commit()
        # Update rooms table with latest tariff and tax
        self.cursor.execute('UPDATE rooms SET tariff = %s, tariff_tax = %s WHERE roomid = %s', (tariff, tariff_tax, roomid))
        self.conn.commit()
        total_amount = (tariff + tariff_tax) - payadvance
        print(f"✅ Advance booking done for room ID {roomid}")
        print(f"Advance Paid: {payadvance}")
        print(f"Tariff: {tariff}, Tax: {tariff_tax}")
        print(f"Total Amount to Pay at Check-in: {total_amount}")

    def cancel_advance_booking(self, booking_id):
        self.cursor.execute("SELECT booking_type, checked_out FROM bookings WHERE id = %s", (booking_id,))
        result = self.cursor.fetchone()
        if not result:
            print("❌ Booking not found.")
            return
        if result[0] != "advance":
            print("❌ Not an advance booking.")
            return
        if result[1]:
            print("❌ Cannot cancel, already checked out.")
            return
        self.cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        self.conn.commit()
        print(f"✅ Advance booking {booking_id} cancelled.")

    def run(self):
        while True:
            print("\n📋 Booking Menu:")
            print("1. Advance Booking")
            print("2. Cancel Advance Booking")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")
            if choice == "1":
                try:
                    roomid = int(input("Enter room ID: "))
                    details = self.get_customer_details()
                    self.advance_room_booking(roomid, *details)
                except Exception as e:
                    print("❌ Error:", e)
            elif choice == "2":
                try:
                    booking_id = int(input("Enter advance booking ID to cancel: "))
                    self.cancel_advance_booking(booking_id)
                except Exception as e:
                    print("❌ Error:", e)
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    booking = Booking()
