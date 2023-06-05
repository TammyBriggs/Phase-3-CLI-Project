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
    number = Column(String(20))
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
        print("Adding a bus")

    elif choice == 2:
        print("Looking for a bus")


# Entry point
if __name__ == '__main__':
    Base.metadata.create_all(engine)
