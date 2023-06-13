# Inventory Management System
Inventory Management Web Application
This is a Django-based web application that provides users with a dashboard to view insights and analytics about inventory items. The application allows users to scan QR and barcodes of inventory items to update the MySQL database, which is used to generate the insights.

## Features
* Scanning QR and barcodes of inventory items to update the database
* Dashboard displaying insights and analytics about inventory items
* SQL database for storing inventory data
* User authentication and access control

## Setup
* Clone the repository
```https://github.com/Zeeshanzt/Intelligent-Systems.git```

* Navigate to the project directory
```cd Intelligent-Systems```
* Install the dependencies
```pip install -r requirements.txt```
* Run the migrations
```python manage.py migrate```
* Create a Superuser
```python manage.py createsuperuser```
* Start the development server
```python manage.py runserver```
## Usage
* Open a web browser and navigate to http://localhost:8000/
* Login using your username and password
* Scan the images taken by drone during flight time and provide its path to web application
* The inventory item will be updated in the MySQL database and the dashboard will display insights and analytics about the item after you press process images button in the web application
