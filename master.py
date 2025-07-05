import mysql.connector
from mysql.connector import Error

class MasterConfiguration:

    def __init__(self):
        self.cursor = None
        try:
            self.con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='santho25.08',
                database='hoteldesk_management_system'  # Ensure this database exists
            )
            self.cursor = self.con.cursor()
            self.table()
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")

    def table(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS floor_master (
                floorid INT PRIMARY KEY,
                floor_name VARCHAR(255),
                room_count INT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roomid INT UNIQUE,
                room_type VARCHAR(255),
                room_count_cat VARCHAR(255)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                roomid INT PRIMARY KEY,
                room_type VARCHAR(255),
                room_number VARCHAR(255),
                tariff INT,
                tariff_tax INT,
                room_status VARCHAR(255),
                FOREIGN KEY (roomid) REFERENCES room_category (roomid)
            )
        ''')
        self.con.commit()

    def add_floor(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        try:
            floorid = int(input("Enter floor ID: "))
            floor_name = input("Enter floor name: ")
            room_count = int(input("Enter room count: "))

            self.cursor.execute('''
                INSERT INTO floor_master (floorid, floor_name, room_count)
                VALUES (%s, %s, %s)
            ''', (floorid, floor_name, room_count))

            self.con.commit()
            print("✅ Floor added.")
        except Error as e:
            print("❌ Floor already exists or constraint failed.", e)
        except Exception as e:
            print("❌ Error:", e)

    def add_room_category(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        try:
            roomid = int(input("Enter room ID: "))
            room_type = input("Enter room type: ")
            room_count_cat = input("Enter room count in category: ")

            self.cursor.execute('''
                INSERT INTO room_category (roomid, room_type, room_count_cat)
                VALUES (%s, %s, %s)
            ''', (roomid, room_type, room_count_cat))

            self.con.commit()
            print("✅ Room category added.")
        except Error as e:
            print("❌ Room ID already exists or constraint failed.", e)
        except Exception as e:
            print("❌ Error:", e)

    def add_room(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        try:
            roomid = int(input("Enter room ID (must match room_category): "))
            room_type = input("Enter room type: ")
            room_number = input("Enter room number: ")
            tariff = int(input("Enter room tariff: "))
            tariff_tax = int(input("Enter tariff tax: "))
            room_status = input("Enter room status (Available/Occupied): ")

            self.cursor.execute('''
                INSERT INTO rooms (roomid, room_type, room_number, tariff, tariff_tax, room_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (roomid, room_type, room_number, tariff, tariff_tax, room_status))

            self.con.commit()
            print("✅ Room added.")
        except Error as e:
            print("❌ Error: Room ID exists or doesn't match category.", e)
        except Exception as e:
            print("❌ Error:", e)

    def view_data(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        print("\nView Options:")
        print("1. View Floors")
        print("2. View Room Categories")
        print("3. View Rooms")

        option = input("Enter option (1-3): ")
        if option == "1":
            self.cursor.execute("SELECT * FROM floor_master")
        elif option == "2":
            self.cursor.execute("SELECT * FROM room_category")
        elif option == "3":
            self.cursor.execute("SELECT * FROM rooms")
        else:
            print("Invalid option.")
            return

        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")

    def delete_data(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        print("\nDelete Options:")
        print("1. Delete Floor")
        print("2. Delete Room Category")
        print("3. Delete Room")

        option = input("Enter option (1-3): ")
        try:
            if option == "1":
                floorid = int(input("Enter floor ID: "))
                self.cursor.execute("SELECT * FROM floor_master WHERE floorid = %s", (floorid,))
                if self.cursor.fetchone():
                    self.cursor.execute("DELETE FROM floor_master WHERE floorid = %s", (floorid,))
                else:
                    print("❌ Floor not found.")
                    return

            elif option == "2":
                roomid = int(input("Enter room ID: "))
                self.cursor.execute("SELECT * FROM room_category WHERE roomid = %s", (roomid,))
                if self.cursor.fetchone():
                    self.cursor.execute("DELETE FROM room_category WHERE roomid = %s", (roomid,))
                else:
                    print("❌ Room category not found.")
                    return

            elif option == "3":
                roomid = int(input("Enter room ID: "))
                self.cursor.execute("SELECT * FROM rooms WHERE roomid = %s", (roomid,))
                if self.cursor.fetchone():
                    self.cursor.execute("DELETE FROM rooms WHERE roomid = %s", (roomid,))
                else:
                    print("❌ Room not found.")
                    return

            else:
                print("Invalid option.")
                return

            self.con.commit()
            print("✅ Record deleted.")
        except Exception as e:
            print("❌ Error deleting record:", e)

    def update_data(self):
        if not self.cursor:
            print("❌ No database connection.")
            return
        print("\nUpdate Options:")
        print("1. Update Floor")
        print("2. Update Room Category")
        print("3. Update Room")

        option = input("Enter option (1-3): ")

        try:
            if option == "1":
                floorid = int(input("Enter floor ID to update: "))
                self.cursor.execute("SELECT * FROM floor_master WHERE floorid = %s", (floorid,))
                if not self.cursor.fetchone():
                    print("❌ Floor not found.")
                    return

                new_name = input("Enter new floor name: ")
                new_count = int(input("Enter new room count: "))
                self.cursor.execute("UPDATE floor_master SET floor_name = %s, room_count = %s WHERE floorid = %s", (new_name, new_count, floorid))

            elif option == "2":
                roomid = int(input("Enter room ID to update: "))
                self.cursor.execute("SELECT * FROM room_category WHERE roomid = %s", (roomid,))
                if not self.cursor.fetchone():
                    print("❌ Room category not found.")
                    return

                new_type = input("Enter new room type: ")
                new_count = input("Enter new room count in category: ")
                self.cursor.execute("UPDATE room_category SET room_type = %s, room_count_cat = %s WHERE roomid = %s", (new_type, new_count, roomid))

            elif option == "3":
                roomid = int(input("Enter room ID to update: "))
                self.cursor.execute("SELECT * FROM rooms WHERE roomid = %s", (roomid,))
                if not self.cursor.fetchone():
                    print("❌ Room not found.")
                    return

                new_type = input("Enter new room type: ")
                new_number = input("Enter new room number: ")
                new_tariff = int(input("Enter new tariff: "))
                new_tariff_tax = int(input("Enter new tariff tax: "))
                new_status = input("Enter new room status: ")
                self.cursor.execute("UPDATE rooms SET room_type = %s, room_number = %s, tariff = %s, tariff_tax = %s, room_status = %s WHERE roomid = %s", (new_type, new_number, new_tariff, new_tariff_tax, new_status, roomid))
            else:
                print("Invalid option.")
                return

            self.con.commit()
            print("✅ Record updated.")
        except Exception as e:
            print("❌ Error updating record:", e)

    def run(self):
        if not self.cursor:
            print("❌ Cannot run master configuration: No database connection.")
            return
        while True:
            print("\n📋 Masters:")
            print("1. Add Floor")
            print("2. Add Room Category")
            print("3. Add Room")
            print("4. View Data")
            print("5. Delete Data")
            print("6. Update Data")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self.add_floor()
            elif choice == "2":
                self.add_room_category()
            elif choice == "3":
                self.add_room()
            elif choice == "4":
                self.view_data()
            elif choice == "5":
                self.delete_data()
            elif choice == "6":
                self.update_data()
            elif choice == "7":
                print("Exiting. 👋")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    ho = MasterConfiguration()
    
