# Little Lemon Restaurant - Full-Stack Web Application & API

A full-stack web application and RESTful API developed as the final capstone project for the Meta Back-End Developer Professional Certificate. The project features full authentication, role-based access control (RBAC), database seeding, cart and order management, booking reservation management, and a responsive frontend template.

**Live Deployment URL:** [https://littlelemon-restaurant-b435.onrender.com](https://littlelemon-restaurant-b435.onrender.com)

---

## 📌 Project Overview

The Little Lemon app allows customers to view menu items, register accounts, manage shopping carts, reserve tables, and place orders. The API implements role-based permissions to distinguish between regular **Customers**, **Delivery Crew**, **Managers**, and **Superusers (Admins)**.

### Key Features
* **Authentication & User Management:** Handled via Djoser and Django REST Framework Token Authentication.
* **Menu Management:** Endpoints for browsing, adding, updating, and deleting menu items.
* **Cart, Orders & Bookings:** Complete customer ordering and table reservation workflows.
* **Role-Based Access Control (RBAC):** Group permissions restricting administrative endpoints to Managers/Admins and delivery status updates to Delivery Crew.
* **Database Persistence on Render:** Production database automatically seeded via `initial_data.json` fixture during build execution.

---

## 🛠️ Tech Stack & Tools

* **Backend Framework:** Django 4.x & Django REST Framework (DRF)
* **Authentication:** Djoser (Token-based Auth)
* **Database:** SQLite (Development & Production via Fixtures)
* **Hosting Platform:** Render (Web Service with Automated Build Script)
* **API Testing Tool:** Insomnia

---

## 🔑 Test Credentials & Roles

Evaluators can use the following pre-configured credentials to test role-based permissions across endpoints:

- **Admin / Superuser:**
  - Username: `admin`
  - Password: `admin1234`
- **Manager:**
  - Username: `manager`
  - Password: `manpass1234`
- **Delivery Crew:**
  - Username: `delivery_crew`
  - Password: `crewpass1234`
- **Customer:**
  - Username: `customer`
  - Password: `cuspass1234`

---

## 🚀 API & Application Endpoint Reference

### 1. Authentication & Users
* `POST /auth/users/` — Register a new customer account (Djoser).
* `POST /auth/token/login/` — Submit credentials (`username`, `password`) to receive `auth_token` (Djoser).
* `POST /auth/token/logout/` — Logout and invalidate token (Djoser).
* `GET /users/` — User management view (`UserView`).

### 2. Menu Items & Orders
* `GET /menu-items/` — List all menu items (`MenuView`).
* `GET /orders/` — List orders (`OrderView`).
* `GET /orders/<int:pk>/` — Retrieve single order detail (`SingleOrderView`).
* `GET /order-items/` — List individual order items (`OrderItemView`).

### 3. User Group & Role Management (`/groups/`)
* `GET / POST /groups/manager/users/` — List or assign users to Manager group (`ManagerGroupView`).
* `DELETE /groups/manager/users/<int:pk>/` — Remove user from Manager group (`ManagerGroupDeleteView`).
* `GET / POST /groups/delivery-crew/users/` — List or assign users to Delivery Crew group (`DeliveryCrewGroupView`).
* `DELETE /groups/delivery-crew/users/<int:pk>/` — Remove user from Delivery Crew group (`DeliveryCrewDeleteView`).

### 4. Cart & Bookings
* `GET / POST / DELETE /cart/menu-items/` — Manage customer cart items (`CartView`).
* `GET / POST /bookings/` — List or create table bookings (`BookingView`).
* `GET / PUT / DELETE /bookings/<int:pk>/` — Manage specific booking (`SingleBookingView`).

### 5. Frontend Web Views (HTML Templates)
* `GET /` — Home page (`IndexView`, named `'index'`).
* `GET /menu/` — Web menu page (`MenuListView`, named `'menu-items'`).
* `GET /signup/` — Sign-up page (`SignUpView`, named `'signup'`).
* `GET /cart/` — Cart management page (`CartListView`, named `'cart'`).
* `GET /checkout/` — Checkout page (`CheckoutView`, named `'checkout'`).
* `GET /order-success/` — Order completion confirmation page (`OrderSuccessView`, named `'order-success'`).

---

## 🧪 Testing with Insomnia

An exported Insomnia workspace collection is included in this repository: `Insomnia_Collection.json`.

1. Launch **Insomnia**.
2. Click **Preferences / Workspace** -> Select **Import**.
3. Choose `Insomnia_Collection.json` from the root directory of this repository.
4. **Header Setup for Protected Requests:**
   * **Header Name:** `Authorization`
   * **Header Value:** `Token <your_auth_token_here>` *(Note the space between `Token` and the key string)*.

---

## 💻 Local Installation & Setup

To run the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/LittleLemonCapstone.git](https://github.com/YOUR_USERNAME/LittleLemonCapstone.git)
   cd LittleLemonCapstone