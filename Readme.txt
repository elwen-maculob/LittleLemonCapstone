====================================================================
LITTLE LEMON RESTAURANT CAPSTONE PROJECT - PEER REVIEW GUIDE
====================================================================

Welcome reviewers! This document provides a complete guide to navigating 
and testing both the web interface and the REST API endpoints for the 
Little Lemon project, featuring Role-Based Access Control (RBAC), 
authentication, and database portability.

--------------------------------------------------------------------
1. QUICK START & SETUP FOR REVIEWERS
--------------------------------------------------------------------
1. Clone the repository:
   git clone https://github.com/elwen-maculob/LittleLemonCapstone.git
   cd LittleLemonCapstone

2. Create and activate a virtual environment:
   python3 -m venv env
   source env/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Apply migrations and load pre-populated test data:
   python3 manage.py migrate
   python3 manage.py loaddata initial_data.json

5. Run the local development server:
   python3 manage.py runserver

--------------------------------------------------------------------
2. WEB INTERFACE NAVIGATION (HTML & BROWSER TESTING)
--------------------------------------------------------------------
Open your browser and navigate to http://127.0.0.1:8000/ to test the 
front-end views and user flows:

* Landing & Index:
  - GET http://127.0.0.1:8000/ -> Welcome home page (IndexView)

* User Authentication UI:
  - GET/POST http://127.0.0.1:8000/login/ -> Custom login interface
  - GET/POST http://127.0.0.1:8000/signup/ -> User registration view
  - POST http://127.0.0.1:8000/logout/ -> Secure session termination

* Customer Experience:
  - GET http://127.0.0.1:8000/menu/ -> Public menu items list view
  - GET http://127.0.0.1:8000/cart/ -> Customer shopping cart management
  - GET http://127.0.0.1:8000/checkout/ -> Order checkout interface
  - GET http://127.0.0.1:8000/order-success/ -> Order confirmation view

--------------------------------------------------------------------
3. REST API ENDPOINTS (FOR INSOMNIA / POSTMAN TESTING)
--------------------------------------------------------------------
Test these API endpoints using Insomnia or Postman. Remember to include 
your Token authentication header (`Authorization: Token <your_token>`) 
for restricted endpoints.

* Menu Management:
  - GET / POST / PUT / PATCH / DELETE: http://127.0.0.1:8000/api/menu-items

* Cart Operations:
  - GET / POST / DELETE: http://127.0.0.1:8000/api/cart/menu-items

* Order Management:
  - GET / POST: http://127.0.0.1:8000/api/orders
  - GET / PUT / PATCH / DELETE: http://127.0.0.1:8000/api/orders/<int:pk>
  - GET / POST: http://127.0.0.1:8000/api/order-items

* Table Bookings:
  - GET / POST: http://127.0.0.1:8000/api/bookings
  - GET / PUT / PATCH / DELETE: http://127.0.0.1:8000/api/bookings/<int:pk>

* User & Role-Based Access Control (RBAC) - Manager / Crew Management:
  - GET / POST: http://127.0.0.1:8000/api/users
  - GET / POST: http://127.0.0.1:8000/api/groups/manager/users
  - DELETE: http://127.0.0.1:8000/api/groups/manager/users/<int:pk>
  - GET / POST: http://127.0.0.1:8000/api/groups/delivery-crew/users
  - DELETE: http://127.0.0.1:8000/api/groups/delivery-crew/users/<int:pk>

* Authentication & Tokens:
  - POST http://127.0.0.1:8000/auth/users/ (Djoser registration)
  - POST http://127.0.0.1:8000/auth/token/login/ (Obtain token)
  - POST http://127.0.0.1:8000/auth/token/logout/ (Destroy token)

--------------------------------------------------------------------
4. RUNNING AUTOMATED TESTS
--------------------------------------------------------------------
To verify unit tests and system functionality, run:
python3 manage.py test
====================================================================