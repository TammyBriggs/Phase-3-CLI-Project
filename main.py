# Necessary Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

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

#CLI Menu
def main():
    choice = 0
    while choice !=12:
        print("*** Waste Disposal Management ***")
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
        choice = int(input())

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

        # elif choice == 7:
        #     update_bus_route()
        #     break

        # elif choice == 8:
        #     display_all_routes()
        #     break

        # elif choice == 9:
        #     lookup_driver()
        #     break

        # elif choice == 10:
        #     update_bus_driver()
        #     break

        # elif choice == 11:
        #     display_all_drivers()
        #     break

        elif choice == 12:
            print("Quitting Program")
            break

    print("Program Terminated")

#CLI Menu Methods
def add_bus():
    plate_number = input("Enter the plate number of the bus: ")
    
    # Check if the bus with the given plate number already exists
    existing_bus = session.query(Bus).filter_by(plate_number=plate_number).first()
    if existing_bus:
        print("Error: Bus with the same plate number already exists!")
        return

    driver_name = input("Enter the name of the driver: ")

    # Check if the driver is already assigned to three buses
    driver = session.query(Driver).filter_by(name=driver_name).first()
    if driver:
        assigned_buses_count = session.query(Bus).filter_by(driver=driver).count()
        if assigned_buses_count >= 3:
            print("Error: The driver is already assigned to three buses!")
            return
    else:
        driver = Driver(name=driver_name)
        session.add(driver)
        session.commit()

    route_path = input("Enter the route path (e.g., here - here): ")
    
    # Check if the route with the given path already exists
    existing_route = session.query(Route).filter_by(path=route_path).first()
    if existing_route:
        print("Error: Route with the same path already exists!")
        return

    route = Route(path=route_path)
    session.add(route)
    session.commit()

    now = datetime.utcnow()
    datetime_str = now.strftime("%Y-%m-%d %H:%M")
    bus = Bus(plate_number=plate_number, route=route, driver=driver, datetime=datetime_str)
    session.add(bus)
    session.commit()

    print("Bus added successfully!")

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
    else:
        print("Route not found!")

# Entry point
if __name__ == '__main__' or __file__ == 'main.py':
    Base.metadata.create_all(engine)
    main()
