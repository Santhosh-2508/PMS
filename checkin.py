import mysql.connector
from mysql.connector import Error
from datetime import datetime

class CheckIn:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='santho25.08',
                database='hoteldesk_management_system'
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")

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

    def direct_checkin(self, roomid, *details):
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
            discount_percent = float(input("Enter discount percentage (0 if none): "))
            if discount_percent < 0 or discount_percent > 100:
                print("❌ Invalid discount percentage.")
                return
        except ValueError:
            print("❌ Invalid input.")
            return
        discount = ((tariff or 0) + (tariff_tax or 0)) * (discount_percent / 100)
        total_amount = (tariff or 0) + (tariff_tax or 0) - payadvance - discount
        checkin = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        checkout = input("Enter check-out datetime (YYYY-MM-DD HH:MM:SS): ")
        booking_datetime = checkin
        self.cursor.execute('''
            INSERT INTO bookings (
                booking_type, roomid, customer_name, customer_phone, customer_email,
                customer_address, customer_city, customer_state, customer_gender,
                checkin_datetime, checkout_datetime, booking_datetime, payadvance, tariff, tariff_tax, discount, total_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', ("direct", roomid, *details, checkin, checkout, booking_datetime, payadvance, tariff, tariff_tax, discount, total_amount))
        self.conn.commit()
        print(f"✅ Direct check-in done for room ID {roomid}")
        print(f"Advance Paid: {payadvance}")
        print(f"Tariff: {tariff}, Tax: {tariff_tax}")
        print(f"Discount: {discount} ({discount_percent}%)")
        print(f"Total Amount to Pay: {total_amount}")

    def run(self):
        while True:
            print("\n📋 Direct Check-In Menu:")
            print("1. Direct Check-In")
            print("2. Exit")
            choice = input("Enter your choice (1-2): ")
            if choice == "1":
                try:
                    roomid = int(input("Enter room ID: "))
                    details = self.get_customer_details()
                    self.direct_checkin(roomid, *details)
                except Exception as e:
                    print("❌ Error:", e)
            elif choice == "2":
                break
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    checkin = CheckIn()
