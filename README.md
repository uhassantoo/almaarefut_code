# Zubies E-commerce Project

This is a Django-based e-commerce application that provides functionalities for users to browse products, add them to wishlist, add them to the cart, proceed with the checkout process, save multiple addresses, and check order history.

## Features

- User registration and authentication
- Product listing and detail views
- Wishlist management
- Shopping cart management
- Order management
- Admin interface for product and order management

## Prerequisites

- Python 3.12+
- Django 5.0+
- SQLite3 (default Django database)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tmalik258/Zubies.git
   cd Zubies
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files:**

   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` in your browser to see the application running.

## Configuration

### Email Configuration

For email functionalities such as password reset, configure the email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin` to manage products and orders.
- Register as a user to browse products, add them to the cart, and proceed with checkout.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request
