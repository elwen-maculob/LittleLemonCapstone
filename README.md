# Little Lemon Restaurant API

A robust RESTful API built with **Django** and **Django REST Framework (DRF)** for restaurant reservations, menu item management, and order processing. Built with Role-Based Access Control (RBAC), token authentication, and data serialization.

---

## 🚀 Key Features

- **User Authentication:** Token-based security using Djoser and DRF authentication.
- **Role-Based Access Control (RBAC):** Group permissions separating `Manager`, `Delivery Crew`, and `Customer` access levels.
- **Menu & Order Management:** Full CRUD operations for menu items, category filtering, search, and ordering pipeline.
- **Table Booking API:** Reservation management with date/time slot conflict validation.

---

## 🛠️ Tech Stack & Tools

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite / MySQL
- **Authentication:** Token / Djoser
- **Testing & API Documentation:** Postman, Insomnia, Pytest

---

## ⚙️ Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/elwen-maculob/LittleLemonCapstone.git
cd LittleLemonCapstone

---
## Test Credentials & Roles

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