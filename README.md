
Vendor Management System
The Vendor Management System is a Django-based application designed to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.
Author_Pratik Pattanaik

Setup
1.Clone the repository:
    git clone https://github.com/yourusername/vendor-management-system.git


2.Navigate to the project directory:
    cd vendor-management-system


3.Install dependencies:
    pip install -r requirements.txt


4.Apply database migrations:
    python manage.py migrate



5.Create a superuser to access the admin panel:
    python manage.py createsuperuser



6.Run the development server:
    python manage.py runserver
    
    Access the application in your web browser at http://127.0.0.1:8000/


7.Testing
    To run tests:
    python manage.py test



API Endpoints
Vendor Profile Management
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
Purchase Order Tracking
POST /api/purchase_orders/: Create a purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
Vendor Performance Evaluation
GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.

