import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Checkout:
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

    def checkout(self, booking_id):
        self.cursor.execute("SELECT checked_out, total_amount FROM bookings WHERE id = %s", (booking_id,))
        result = self.cursor.fetchone()
        if not result:
            print("❌ Booking not found.")
            return
        if result[0]:
            print("❌ Already checked out.")
            return
        total_amount = result[1] if result[1] is not None else 0
        try:
            discount_percent = float(input("Enter discount percentage for checkout (0 if none): "))
            if discount_percent < 0 or discount_percent > 100:
                print("❌ Invalid discount percentage.")
                return
        except ValueError:
            print("❌ Invalid discount percentage.")
            return
        discount = total_amount * (discount_percent / 100)
        discounted_total = total_amount - discount
        print(f"Total amount to pay before checkout: {total_amount}")
        print(f"Discount: {discount} ({discount_percent}%)")
        print(f"Amount to pay after discount: {discounted_total}")
        try:
            paid = int(input("Enter amount paid: "))
            if paid < discounted_total:
                print(f"❌ Insufficient payment. {discounted_total - paid} still due.")
                return
        except ValueError:
            print("❌ Invalid payment amount.")
            return
        checkout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("UPDATE bookings SET checked_out = 1, checkout_datetime = %s, discount = %s, total_amount = %s WHERE id = %s", (checkout_time, discount, discounted_total, booking_id))
        self.conn.commit()
        print(f"✅ Booking {booking_id} checked out at {checkout_time}")
