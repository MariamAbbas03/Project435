# PROJECT 435

Our project is a simple ecommerce application with three main services: Customers, Inventory, and Sales.

## Table of Contents

- [Overview](#overview)
- [Databases](#databases)
- [Applications](#applications)
- [API Endpoints](#api-endpoints)
- [Contribution](#contribution)

## Overview

This e-commerce application consists of three databases: `ecommerce_customers.db`, `ecommerce_inventory.db`, and `ecommerce_sales.db`. 
Each database serves a specific purpose related to customer management, inventory tracking, and sales transactions.

## Databases

### 1. ecommerce_customers.db

- Manages customer information.
- Table: `customers` with fields: `customer_id`, `full_name`, `username`, `password`, `age`, `address`, `gender`, `marital_status`, `wallet_balance`.

### 2. ecommerce_inventory.db

- Manages inventory information.
- Table: `inventory` with fields: `item_id`, `name`, `category`, `price_per_item`, `description`, `count_in_stock`.

### 3. ecommerce_sales.db

- Manages sales transactions.
- Table: `sales` with fields: `sale_id`, `customer_id`, `item_id`, `sale_date`.

## Applications

### 1. Customers Application

- Provides API endpoints for customer-related operations.
- Endpoints include customer registration, retrieval of all customers, retrieval of a customer by username, updating customer information, deleting a customer, charging a customer's wallet, and deducting money from a customer's wallet.

### 2. Inventory Application

- Provides API endpoints for inventory-related operations.
- Endpoints include adding an item to the inventory, retrieving all items, retrieving an item by ID, updating item information, and deducting stock of an item.

### 3. Sales Application

- Provides API endpoints for managing sales transactions.
- Endpoints include making a sale (which involves checking customer wallet balance and item stock) and retrieving sales information for a specific customer.

## API Endpoints

Refer to each application's source code for a detailed list of API endpoints.
we will also provide a postman collection for each application to test the API calls

## Contributing

This project was done by Mariam Abbas and Mahdi Ajrouch
