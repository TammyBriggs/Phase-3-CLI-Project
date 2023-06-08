# Phase-3-CLI-Project

# Waste Disposal Management DBMS oversees the smooth running of a waste disposal management company, 09/06/2023

#### By **Tamunotonye Briggs**

## Description
This program is a Waste Disposal Management Database Management System (DBMS) implemented using Python and SQLAlchemy. It allows you to manage buses, routes, and drivers involved in waste management operations.

## Features
- Add a bus: Add a new bus to the system by providing the plate number, driver name, and route path.
- Lookup a bus: Find detailed information about a specific bus using its plate number.
- Update a bus plate number: Update the plate number of a bus.
- Delete a bus: Delete a bus from the system along with its associated driver and route.
- Display all buses: Show a list of all buses in the system with their details.
- Lookup a route: Find detailed information about a specific route using its path.
- Update a bus route: Update the route of a bus.
- Display all routes: Show a list of all routes in the system with their details.
- Lookup a driver: Find detailed information about a specific driver using their name.
- Update a bus driver: Update the driver of a bus.
- Display all drivers: Show a list of all drivers in the system with their details.
- Generate reports:
  - Generate a report on the busiest driver(s) and the number of buses they are driving.
  - Generate a report on the date with the most active buses.

## Getting Started
1. Clone the repository: `git clone <repository_url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the program: `python main.py`

## Usage
Upon running the program, a menu will be displayed with various options. Use the provided numbers to select an option and interact with the system.

For example, to add a new bus:
1. Choose "1) Waste-Management DBMS Menu" from the main menu.
2. Choose "1) Add a bus" from the Waste-Management DBMS Menu.
3. Enter the plate number, driver name, and route path when prompted.

Follow the menu options to perform other actions such as looking up buses, updating information, displaying lists, and generating reports.

## Database
The program uses an SQLite database named `waste-management.db`. The database file will be created automatically when you run the program for the first time. No additional setup is required.

### License
This project is licensed under the [MIT License](LICENSE). See `LICENSE` for more information.
