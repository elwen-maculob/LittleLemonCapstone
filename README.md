# Little Lemon Restaurant API Project
Capstone project for the Back-End Developer Professional Certificate, featuring a Django REST API with Role-Based Access Control (RBAC), database synchronization, and data portability.

## Project Setup & Installation

1. Clone the Repository:
   ```bash
   git clone https://github.com/elwen-maculob/LittleLemonCapstone.git
   cd LittleLemonCapstone

```
2. Create and activate a virtual environment:
```bash
python3 -m venv env
source env/bin/activate

```
3. Install dependencies:
```bash
pip install -r requirements.txt

```
## Database & Migrations

1. Run migrations to set up the database schema:
```bash
python3 manage.py migrate

```
2. Load the initial data fixture (includes categories, menu items, and roles):
```bash
python3 manage.py loaddata initial_data.json

```
## Running the Server & Tests

1. Start the development server:
```bash
python3 manage.py runserver

```
2. Run the test suite to verify functionality:
```bash
python3 manage.py test

```
## Role-Based Access Control (RBAC)

* Managers: Full administrative control over menu items, orders, and user group management.
* Delivery Crew: Access to view and update delivery status on assigned order items.
* Customers: Access to view menu items, manage cart, and place orders.