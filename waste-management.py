import click
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
    datetime = Column(DateTime, default=datetime.utcnow)

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    buses = relationship("Bus", back_populates="route")


class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    buses = relationship("Bus", back_populates="driver")

@click.command()
def main():
    choice = 0
    while choice !=10:
        print("*** Waste Disposal Management ***")
        print("1) Add a bus")
        print("2) Lookup a bus")
        print("3) Display all buses")
        print("4) Add a Route")
        print("5) Lookup a Route")
        print("6) Display all routes")
        print("7) Add a driver")
        print("8) Lookup a driver")
        print("9) Display all drivers")
        print("10) Quit")
        choice = int(input())

        if choice == 1:
            add_bus()
            break

        elif choice == 2:
            lookup_bus()
            break

        elif choice == 3:
            print("Displaying all buses")
            break

        elif choice == 4:
            print("Adding a route")
            break

        elif choice == 5:
            print("Looking for a route")
            break

        elif choice == 6:
            print("Displaying all routes")
            break

        elif choice == 7:
            print("Adding a driver")
            break

        elif choice == 8:
            print("Looking for a driver")
            break

        elif choice == 9:
            print("Displaying all drivers")
            break

        elif choice == 10:
            print("Quitting Program")
            break

    print("Program Terminated")

def add_bus():
    plate_number = input("Enter the plate number of the bus: ")
    route_id = int(input("Enter the route ID of the bus: "))
    driver_id = int(input("Enter the driver ID of the bus: "))

    bus = Bus(plate_number=plate_number, route_id=route_id, driver_id=driver_id)
    session.add(bus)
    session.commit()
    print("Bus added successfully!")


def lookup_bus():
    plate_number = input("Enter the plate number of the bus to lookup: ")
    bus = session.query(Bus).filter_by(plate_number=plate_number).first()

    if bus:
        print("Bus found!")
        print("Plate Number:", bus.plate_number)
        print("Route ID:", bus.route_id)
        print("Driver ID:", bus.driver_id)
        print("Datetime:", bus.datetime)
    else:
        print("Bus not found!")

# Entry point
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    main()
