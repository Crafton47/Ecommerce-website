# 🛒 Vibrant E-Commerce Website

A full-stack e-commerce web application built with **Python Flask**, **SQLite**, and a **Java currency converter API**.

---

## 🚀 Features

- 🏠 **Home Page** — Interactive image accordion with auto-rolling animation
- 🛍️ **Products Page** — Mobiles, Laptops, Watches, Books, Groceries, Gaming Laptops
- 🛒 **Shopping Cart** — Add/remove items, quantity control, order summary
- 🔐 **Authentication** — Sign up, Login, Logout with hashed passwords
- 💱 **Currency Converter** — Powered by a Java HTTP server (INR → USD, EUR, GBP, JPY)
- 💳 **Payment Modal** — Cash on Delivery & Credit/Debit Card (mock)
- 📦 **Order Placement** — Address input and order success animation

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask |
| Database | SQLite (via Flask-SQLAlchemy) |
| Auth | Werkzeug password hashing |
| Java API | Java HttpServer (built-in) |

---

## 📁 Project Structure

```
Ecommerce-website/
├── app.py                  # Flask application
├── java-api/
│   └── CurrencyServer.java # Java currency converter API
├── static/
│   └── style.css           # All styles
├── templates/
│   ├── Ecommerce.html      # Home page
│   ├── products.html       # Products page
│   ├── cart.html           # Cart page
│   ├── login.html          # Login page
│   └── signup.html         # Sign up page
└── .gitignore
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.x
- JDK 17+ (for currency converter)

### 1 — Install Python dependencies

```bash
pip install flask flask-sqlalchemy
```

### 2 — Compile the Java currency server

```bash
cd java-api
javac CurrencyServer.java
```

### 3 — Start the Java server (Terminal 1)

```bash
java CurrencyServer
```

You should see:
```
✅ Currency API running at http://localhost:8080/convert
```

### 4 — Start the Flask app (Terminal 2)

```bash
python app.py
```

### 5 — Open in browser

```
http://127.0.0.1:5000
```

---

## 💱 Currency Converter API

The Java server runs on port `8080` and supports:

```
GET /convert?amount=79900&to=USD
```

**Supported currencies:** USD, EUR, GBP, JPY, INR

**Example response:**
```json
{
  "from": "INR",
  "to": "USD",
  "amount": 79900.0,
  "converted": 958.80,
  "symbol": "$"
}
```

---

## 📸 Pages

- `/` — Home with interactive accordion
- `/products` — All products with currency converter
- `/cart` — Shopping cart with checkout
- `/login` — Login page
- `/signup` — Sign up page

---

## 👤 Author

**Crafton47** — [github.com/Crafton47](https://github.com/Crafton47)
