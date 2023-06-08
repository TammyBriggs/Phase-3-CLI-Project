# Necessary Imports
import click
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from collections import Counter

# Database setup
engine = create_engine('sqlite:///waste-management.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Models
class Bus(Base):
    __tablename__ = 'buses'
    id = Column(Integer, primary_key=True)
    plate_number = Column(String(20))
    route_id = Column(Integer, ForeignKey('routes.id'))
    route = relationship("Route", back_populates="buses")
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    driver = relationship("Driver", back_populates="buses")
    datetime = Column(String(16), default=datetime.utcnow)

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    path = Column(String(100))
    buses = relationship("Bus", back_populates="route")


class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    buses = relationship("Bus", back_populates="driver")

# CLI Menu
@click.command()
def main():
    choice = 0
    while choice != 12:
        print("*** Waste Disposal Management ***")
        print("1) Waste-Management DBMS Menu")
        print("2) Reports")

        while True:
                try:
                    choice = int(input("Enter your choice: "))
                    if choice not in [1, 2]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please try again.")

        if choice == 1:
            print("*** Waste-Management DBMS Menu ***")
            print("1) Add a bus")
            print("2) Lookup a bus")
            print("3) Update a bus plate number")
            print("4) Delete a bus")
            print("5) Display all buses")
            print("6) Lookup a Route")
            print("7) Update a bus route")
            print("8) Display all routes")
            print("9) Lookup a driver")
            print("10) Update a bus driver")
            print("11) Display all drivers")
            print("12) Quit")
            # choice = int(input())

            while True:
                try:
                    choice = int(input("Enter your choice: "))
                    if choice not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please try again.")

            if choice == 1:
                add_bus()
                break

            elif choice == 2:
                lookup_bus()
                break

            elif choice == 3:
                update_bus_plate_number()
                break

            elif choice == 4:
                delete_bus()
                break

            elif choice == 5:
                display_all_buses()
                break

            elif choice == 6:
                lookup_route()
                break

            elif choice == 7:
                update_route()
                break

            elif choice == 8:
                display_all_routes()
                break

            elif choice == 9:
                lookup_driver()
                break

            elif choice == 10:
                update_driver()
                break

            elif choice == 11:
                display_all_drivers()
                break

            elif choice == 12:
                print("Quitting Program")
                break

        elif choice == 2:

            print("*** Report Generation ***")
            print("1) Generate a report on the buisiest driver(s) and how many buses they're driving")
            print("2) Generate a report on the date with the most active buses")
            print("3) Quit")

            while True:
                try:
                    sub_choice = int(input("Enter your choice: "))
                    if sub_choice not in [1, 2, 3]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please try again.")

        if sub_choice == 1:
            busiest_driver()
            break

        elif sub_choice == 2:
            day_with_most_active_buses()
            break

        elif sub_choice == 3:
            print("Returning to the main menu.")
            break

        else:
            print("Invalid choice. Please try again.")

    print("Program Terminated")

#CLI Waste-Management DBMS Menu Methods
def add_bus():
    buses = []

    while True:
        plate_number = input("Enter the plate number of the bus (or 'q' to quit): ")
        if plate_number == 'q':
            break

        # Check if the bus with the given plate number already exists
        existing_bus = session.query(Bus).filter_by(plate_number=plate_number).first()
        if existing_bus:
            print(f"Error: Bus with the plate number '{plate_number}' already exists!")
            continue

        driver_name = input("Enter the name of the driver: ")

        # Check if the driver is already assigned to three buses
        driver = session.query(Driver).filter_by(name=driver_name).first()
        if driver:
            assigned_buses_count = session.query(Bus).filter_by(driver=driver).count()
            if assigned_buses_count >= 3:
                print(f"Error: The driver '{driver_name}' is already assigned to three buses!")
                continue
        else:
            driver = Driver(name=driver_name)
            session.add(driver)
            session.commit()

        route_path = input("Enter the route path (e.g., here - here): ")

        # Check if the route with the given path already exists
        existing_route = session.query(Route).filter_by(path=route_path).first()
        if existing_route:
            print(f"Error: Route with the path '{route_path}' already exists!")
            continue

        route = Route(path=route_path)
        session.add(route)
        session.commit()

        now = datetime.utcnow()
        datetime_str = now.strftime("%Y-%m-%d %H:%M")
        bus = Bus(plate_number=plate_number, route=route, driver=driver, datetime=datetime_str)
        buses.append(bus)

    session.add_all(buses)
    session.commit()

    if plate_number != 'q':
        print("Buses added successfully!")

def lookup_bus():
    plate_number = input("Enter the plate number of the bus to lookup: ")
    bus = session.query(Bus).filter_by(plate_number=plate_number).first()

    if bus:
        print("Bus found!")
        print("Plate Number:", bus.plate_number)
        print("Route Path:", bus.route.path)
        print("Driver Name:", bus.driver.name)
        print("Datetime:", bus.datetime)
    else:
        print("Bus not found!")


def update_bus_plate_number():
    plate_number = input("Enter the plate number of the bus to update: ")
    bus = session.query(Bus).filter_by(plate_number=plate_number).first()

    if bus:
        new_plate_number = input("Enter the new plate number: ")
        bus_with_new_plate = session.query(Bus).filter_by(plate_number=new_plate_number).first()

        if bus_with_new_plate:
            print("Error: Another bus already has the new plate number.")
        else:
            bus.plate_number = new_plate_number
            session.commit()
            print("Bus plate number updated successfully!")
    else:
        print("Error: Bus not found!")

def delete_bus():
    plate_number = input("Enter the plate number of the bus to delete: ")
    bus = session.query(Bus).filter_by(plate_number=plate_number).first()

    if bus:
        driver = bus.driver
        route = bus.route

        session.delete(bus)
        session.delete(driver)
        session.delete(route)

        session.commit()
        print("Bus and associated driver and route deleted successfully!")
    else:
        print("Error: Bus not found!")


def display_all_buses():
    buses = session.query(Bus).all()
    print("All Buses:")
    for bus in buses:
        print("Plate Number:", bus.plate_number)
        print("Route Path:", bus.route.path)
        print("Driver Name:", bus.driver.name)
        datetime_obj = datetime.strptime(bus.datetime, "%Y-%m-%d %H:%M")
        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M")
        print("Datetime:", formatted_datetime)
        print()

def lookup_route():
    route_path = input("Enter the route path to lookup: ")
    route = session.query(Route).filter_by(path=route_path).first()

    if route:
        print("Route found!")
        print("Route ID:", route.id)
        print("Route Path:", route.path)

        buses = route.buses
        if buses:
            print("A Bus is passing that Route!")
            for bus in buses:
                print("Plate Number:", bus.plate_number)
        else:
            print("No buses passing that Route.")
    else:
        print("Route not found!")

def update_route():
    route_path = input("Enter the route path to update: ")
    route = session.query(Route).filter_by(path=route_path).first()

    if not route:
        print("Error: Route not found!")
        return

    new_route_path = input("Enter the new route path: ")
    existing_route = session.query(Route).filter_by(path=new_route_path).first()

    if existing_route:
        print("Error: Another route already has the new route path.")
    else:
        route.path = new_route_path
        session.commit()
        print("Route path updated successfully!")
    
def display_all_routes():
    routes = session.query(Route).all()
    print("All Routes:")
    for route in routes:
        print("Route ID:", route.id)
        print("Route Path:", route.path)
        print()

def lookup_driver():
    driver_name = input("Enter the name of the driver to lookup: ")
    driver = session.query(Driver).filter_by(name=driver_name).first()

    if driver:
        print("Driver found!")
        print("Driver ID:", driver.id)
        print("Driver Name:", driver.name)
    else:
        print("Driver not found!")

def update_driver():
    driver_name = input("Enter the name of the driver: ")
    driver = session.query(Driver).filter_by(name=driver_name).first()

    if driver:
        new_driver_name = input("Enter the new driver name: ")
        if driver_name == new_driver_name:
            print("Error: The new driver name is the same as the existing name!")
            return
        new_driver = session.query(Driver).filter_by(name=new_driver_name).first()
        if new_driver:
            print("Error: Another driver already has the new driver name.")
        else:
            driver.name = new_driver_name
            session.commit()
            print("Driver name updated successfully!")
    else:
        print("Error: Driver not found!")

def display_all_drivers():
    drivers = session.query(Driver).all()
    print("All Drivers:")
    for driver in drivers:
        print("Driver ID:", driver.id)
        print("Driver Name:", driver.name)
        print()

#CLI Reports Methods
def busiest_driver():
    drivers = session.query(Driver).all()
    busiest_driver = max(drivers, key=lambda driver: len(driver.buses))

    print("*** Busiest Driver ***")
    print("Driver Name:", busiest_driver.name)
    print("Number of Buses Assigned:", len(busiest_driver.buses))

def day_with_most_active_buses():
    buses = session.query(Bus).all()

    # Extract the date from the datetime field of each bus
    bus_dates = [bus.datetime.split()[0] for bus in buses]

    # Use Counter to count the occurrences of each date in the bus_dates *list*
    date_counts = Counter(bus_dates)

    # Find the date with the maximum count value in the date_counts *dictionary*
    most_active_date = max(date_counts, key=date_counts.get)
    active_bus_count = date_counts[most_active_date]

    print("*** Day with the most active Buses ***")
    print("Date:", most_active_date)
    print("Active Buses:", active_bus_count)

# Entry point
if __name__ == '__main__' or __file__ == 'main.py':
    Base.metadata.create_all(engine)
    main()
