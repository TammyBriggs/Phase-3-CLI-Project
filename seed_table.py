from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Route, Driver, Bus
import random
from faker import Faker

fake = Faker()

engine = create_engine('sqlite:///waste-management.db')
Session = sessionmaker(bind=engine)
session = Session()

routes = [
    Route(path="Lekki - Ajah"),
    Route(path="Ikeja - Maryland"),
    Route(path="Yaba - Oyingbo"),
    Route(path="Surulere - Ojuelegba"),
    Route(path="Victoria Island - CMS"),
    Route(path="Ikorodu - Mile 12"),
    Route(path="Oshodi - Isolo"),
    Route(path="Festac - Mile 2"),
    Route(path="Berger - Agege"),
    Route(path="Epe - Ijebu-Ode"),
]
session.add_all(routes)
session.commit()

drivers = [
    Driver(name="Rashford"),
    Driver(name="Kevin"),
    Driver(name="Pele"),
    Driver(name="Tyrell"),
    Driver(name="Kai"),
    Driver(name="Henry"),
    Driver(name="Messi"),
    Driver(name="Adam"),
    Driver(name="Rooney"),
    Driver(name="Ronaldo"),
]
session.add_all(drivers)
session.commit()

plates = [
    "ABC 123",
    "DEF 456",
    "GHI 789",
    "JKL 012",
    "MNO 345",
    "PQR 678",
    "STU 901",
    "VWX 234",
    "YZA 567",
    "BCD 890",
    "EFG 123",
    "HIJ 456",
    "KLM 789",
    "NOP 012",
    "QRS 345",
    "TUV 678",
    "WXY 901",
    "ZAB 234",
    "CDE 567",
    "GFK 890"
]

random.shuffle(plates)

for _ in range(20):
    bus = Bus(
        plate_number=plates.pop(),
        route=random.choice(routes),
        driver=random.choice(drivers),
        datetime=fake.date_time_between(start_date='-1y', end_date='now')
    )
    session.add(bus)

session.commit()
