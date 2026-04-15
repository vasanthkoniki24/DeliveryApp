# Real-Time Food Ordering & Tracking System

A full-stack real-time food ordering platform with Admin Dashboard, Order Tracking, and Role-Based Access Control, built using modern technologies.

---

## Project Overview

This application simulates a real-world food delivery system where:

-  Users can browse food items and place orders  
-  Orders are processed and tracked in real-time  
-  Admins can manage products, monitor orders, and update statuses  
-  System ensures proper access control using roles  

---

## Tech Stack

### Backend

- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- WebSockets (real-time updates)  

### Frontend

- React.js  
- Axios  
- Tailwind CSS  
- Framer Motion (animations)  

---

## Features

### User Features

- Register & Login  
- Browse food items with images  
- Search functionality  
- Add to cart  
- Place orders  
- View order history  
- Real-time order tracking  

---

### Order System

- Cart-based ordering  
- Stock validation  
- Idempotent order creation  
- Order lifecycle:  
 
  Created → Confirmed → Processing → Shipped → Delivered
  
---

###  Admin Features

- Admin Dashboard  
- View total orders & revenue  
- Manage products:
  - Add / Edit / Delete  
- Manage orders:
  - Update order status  
  - View all user orders  

---

### Security

- JWT Authentication  
- Role-Based Access Control (Admin / User)  
- Protected routes  

---

## Project Structure

```delivery-app/
│
├── backend/                         # FastAPI Backend
│   │
│   ├── app/
│   │   │
│   │   ├── main.py                 # Entry point of FastAPI app
│   │   │
│   │   ├── core/                   # Core configurations
│   │   │   ├── config.py           # App settings (env variables)
│   │   │   └── security.py         # JWT token creation & hashing
│   │   │
│   │   ├── db/                     # Database setup
│   │   │   ├── base.py             # Base model import
│   │   │   └── session.py          # DB connection (SQLAlchemy)
│   │   │
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── user.py             # User model
│   │   │   ├── product.py          # Product model
│   │   │   ├── order.py            # Order + OrderItem model
│   │   │   └── notification.py     # Notifications model
│   │   │
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── notification.py
│   │   │
│   │   ├── api/                    # API routes
│   │   │   └── v1/
│   │   │       └── routes/
│   │   │           ├── auth.py     # Authentication APIs
│   │   │           ├── product.py  # Product APIs
│   │   │           ├── order.py    # Order APIs
│   │   │           ├── admin.py    # Admin dashboard APIs
│   │   │           └── notification.py
│   │   │
│   │   ├── services/               # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── order_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── order_worker.py     # Background order processing
│   │   │   └── ws_manager.py       # WebSocket manager
│   │   │
│   │   └── dependencies/           # Dependency injections
│   │       └── auth.py             # RBAC & auth dependencies
│   │
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
│
├── frontend/                      # React Frontend
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── axios.js           # Axios instance (base URL, headers)
│   │   │
│   │   ├── assets/                # Images & static files
│   │   │   └── delivery-boy.png   # Login/Register illustration
│   │   │
│   │   ├── components/            # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── pages/                 # Main pages
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Products.jsx       # Home / Food listing
│   │   │   ├── Cart.jsx
│   │   │   ├── Orders.jsx
│   │   │   ├── Tracking.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── ManageProducts.jsx
│   │   │   └── ManageOrders.jsx
│   │   │
│   │   ├── App.js                 # Routes configuration
│   │   ├── index.js               # React entry point
│   │   └── index.css              # Tailwind / global styles
│   │
│   ├── package.json               # Frontend dependencies
│   └── tailwind.config.js         # Tailwind configuration
│
└── README.md                      # Project documentation
---

## Setup Instructions

### 1. Clone the Repository

git clone <your-repo-url>
cd DeliveryApp
---

### 2. Backend Setup

cd backend

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
---

### 3. Configure Database

Update your database connection in:

backend/app/db/session.py
Example:

DATABASE_URL = "postgresql://user:password@localhost/delivery_db"
---

### 4. Run Backend Server

uvicorn app.main:app --reload
- Backend: http://127.0.0.1:9000  
- Swagger Docs: http://127.0.0.1:9000/docs  

---

### 5. Frontend Setup

cd frontend
npm install
npm start
- Frontend: http://localhost:3000  

---

## API Documentation

All APIs are documented using Swagger:

http://127.0.0.1:9000/docs  

---

### Key APIs

#### Auth
- POST /auth/register  
- POST /auth/login  
- GET /auth/me  

#### Products
- GET /products/  
- POST /products/  
- PATCH /products/{id}  
- DELETE /products/{id}  

#### Orders
- POST /orders/  
- GET /orders/  
- GET /orders/{id}  
- PATCH /orders/{id}/status  
- GET /orders/admin/all  

#### Admin
- GET /admin/orders/summary  
- GET /admin/revenue  

---

## Database Schema

### Users
- id  
- email  
- password  
- role  

### Products
- id  
- name  
- description  
- price  
- stock  
- image  

### Orders
- id  
- user_id  
- total_amount  
- status  
- created_at  

### Order Items
- id  
- order_id  
- product_id  
- quantity  
- price  

---

## Frontend Pages

Include:
- Login Page  
- Product Listing  
- Cart Page  
- Order Tracking  
- Admin Dashboard  
- Manage Products  
- Manage Orders  

---

## Testing Notes

- Empty cart orders are blocked  
- Stock reduces on order placement  
- Invalid status transitions are prevented  
- Admin-only routes are protected  
- Idempotency prevents duplicate orders  

---

## Important Notes

- Ensure PostgreSQL is running  
- Update .env before starting backend  
- Use correct roles (admin, customer)  
- Restart backend after schema changes  

---

## Conclusion

This project demonstrates:

-  Real-world system design  
-  Clean API structure  
-  Full frontend-backend integration  
-  Role-based system  
-  Admin monitoring capabilities  