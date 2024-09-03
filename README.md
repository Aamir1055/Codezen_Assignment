E-commerce Platform
Overview
This project is an E-commerce platform built using Django and Celery. It offers a robust set of features for managing products, orders, and users, with automated tasks handled by Celery for efficient operations. The platform supports importing products from Excel files, comprehensive order management, and user role management.

Features
Product Management
Import Products: Import product data from Excel files using pandas.
View and Manage Products: Easily view, update, and manage product details.
Order Management
CRUD Operations: Create, read, update, and delete orders within the platform.
User Management
User Roles: Manage users and assign roles to control access to different parts of the system.
Periodic Tasks
Automation: Automate tasks using Celery with a daily schedule for streamlined operations.
Requirements
Python: 3.8+
Django: 4.0+
Celery: 5.2+
Redis: As the message broker for Celery.
pandas: For handling Excel file imports.
django-celery-beat: For managing periodic tasks within Django.
