# Dine-In Manager - Agile Phased Development Plan

**Phase 1: Core Backend - Table, Menu & Basic Order API**

*   **Focus:** Establish the foundational backend API for managing restaurant data (tables and menu items) **AND include a very basic API for order placement.**  This revised Phase 1 will still be backend-heavy but will deliver a minimal end-to-end flow for order creation.
*   **Features (Revised Phase 1):**
    *   **Backend API Endpoints (Flask):**
        *   **Table Management:**
            *   `POST /tables`: Create a new table (Staff API)
            *   `GET /tables`: List all tables (Staff API)
            *   `GET /tables/{table_id}`: Get details of a specific table (Staff API)
            *   `PUT /tables/{table_id}`: Update table details (Staff API)
            *   `DELETE /tables/{table_id}`: Delete a table (Staff API)
        *   **Menu Management:**
            *   `POST /menu`: Add a new menu item (Staff API)
            *   `GET /menu`: List all menu items (Customer & Staff API)
            *   `GET /menu/{item_id}`: Get details of a specific menu item (Customer & Staff API)
            *   `PUT /menu/{item_id}`: Update menu item details (Staff API)
            *   `DELETE /menu/{item_id}`: Delete a menu item (Staff API)
        *   **Basic Order Management (Simplified for Phase 1):**
            *   `POST /orders`: **Basic Order Creation (Staff API):**  Allow creating an order with minimal details -  initially, we can just focus on associating an order with a table and perhaps a few menu items.  We can simplify the order details for now.
            *   `GET /orders/{order_id}`: Get basic details of a specific order (Staff API) -  just enough to confirm the order was created.
    *   **Database Models (PostgreSQL):** Define models for `Tables`, `Menu`, and **basic `Orders`**.  The `Orders` model in Phase 1 can be simplified to include only essential fields (order ID, table ID, basic order status like "Created"). We can expand the `Orders` model in Phase 3.
    *   **Basic API Documentation:** Use FastAPI's automatic documentation (Swagger UI) for initial API exploration and testing.
*   **Tech Stack (Phase 1 - Revised):** Python, Flask, Flask-SQLAlchemy, PostgreSQL, (FastAPI for initial documentation - though backend will be in Flask)
*   **Testing (Phase 1 - Revised):**
    *   **Unit Tests (Backend - pytest):** Write unit tests for Flask API endpoints, database model interactions, and business logic related to table, menu, **and basic order creation**.
    *   **API Endpoint Testing (Postman/Insomnia):** Manually test all API endpoints including the basic order creation endpoint using Postman or Insomnia.
*   **Demo Deliverables (Phase 1 - Revised):**
    *   Functional backend API for Table and Menu Management **AND basic Order Creation.**
    *   API documentation (Swagger UI) to demonstrate all Phase 1 API endpoints.
    *   Unit tests demonstrating backend code quality and functionality, including basic order creation.

**Phase 2: Staff UI - Table & Menu Management Interface**

*   **Focus:** Develop a basic Staff User Interface (React) to interact with the backend API created in Phase 1 for managing tables and menus. This provides the first interactive component of the application.
*   **Features:**
    *   **React Frontend (Staff UI):**
        *   **Table Management UI:**
            *   View a list of tables.
            *   Create new tables.
            *   Edit existing table details.
            *   Delete tables.
        *   **Menu Management UI:**
            *   View a list of menu items.
            *   Add new menu items.
            *   Edit existing menu item details.
            *   Delete menu items.
    *   **Frontend-Backend API Integration:** Integrate the React Staff UI with the Flask backend API endpoints for table and menu management.
    *   **Debugging and Logging Enhancements:** Implement basic debugging techniques (e.g., print statements, logging) and configure logging levels for different environments to aid in development and troubleshooting in subsequent phases.
*   **Tech Stack (Phase 2):** React, JavaScript, HTML, CSS, Axios (for API calls), (building upon Phase 1 backend stack)
*   **Testing (Phase 2):**
    *   **Frontend Unit Tests (Jest/React Testing Library):** Write unit tests for React components, focusing on UI logic and component behavior in isolation.
    *   **Basic UI Integration Testing (Manual):** Manually test the Staff UI to ensure it correctly interacts with the backend API, data is displayed properly, forms work as expected, and basic error handling is present in the UI.
    *   **End-to-End Testing (Optional - Cypress or similar - basic smoke tests):**  Consider adding very basic end-to-end tests (e.g., using Cypress) to verify the basic flow of creating, editing, and deleting tables and menu items through the UI and API.
*   **Demo Deliverables (Phase 2):**
    *   Functional Staff UI for Table and Menu Management.
    *   Integration with the backend API from Phase 1.
    *   Basic UI tests demonstrating frontend component functionality.

**Phase 3: Order Management - Backend API & Staff UI**

*   **Focus:** Extend the backend API and Staff UI to handle order management. This phase introduces the core ordering functionality for staff.
*   **Features:**
    *   **Backend API Endpoints (Flask):**
        *   **Order Management:**
            *   `POST /orders`: Create a new order (Staff API)
            *   `GET /orders`: List all orders (Staff API)
            *   `GET /orders/{order_id}`: Get details of a specific order (Staff API)
            *   `PUT /orders/{order_id}`: Update order status (Staff API - e.g., "Pending", "In Progress", "Ready", "Served")
            *   `PUT /orders/{order_id}/items`: Add/Update items in an order (Staff API)
            *   `DELETE /orders/{order_id}/items/{item_id}`: Remove item from order (Staff API)
    *   **Database Models (PostgreSQL):** Define `Orders` and `OrderItems` models and relationships.
    *   **Staff UI - Order Management:**
        *   View a list of orders with status.
        *   Create new orders (selecting table and menu items).
        *   Update order status.
        *   View order details (items, status, table).
*   **Tech Stack (Phase 3):**  (Building upon Phase 1 & 2 stacks) + potentially WebSockets for real-time updates (if feasible in this phase, otherwise in Phase 4).
*   **Testing (Phase 3):**
    *   **Unit Tests (Backend):** Extend backend unit tests to cover order management logic and API endpoints.
    *   **Integration Tests (Backend):** Write integration tests to verify the order lifecycle workflow, database interactions for orders, and relationships between tables, menu items, and orders.
    *   **UI Integration Testing (Manual):** Test the Staff UI for order management, ensuring correct interaction with the backend API, order creation, status updates, and data display.
*   **Demo Deliverables (Phase 3):**
    *   Functional backend API for Order Management.
    *   Staff UI for creating and managing orders.
    *   Integration tests for backend order workflow.

**Phase 4: Real-time Order Updates & Basic Customer Menu UI**

*   **Focus:** Implement real-time order status updates using WebSockets and start developing the basic Customer facing UI to view the menu.
*   **Features:**
    *   **Real-time Order Updates (WebSockets):** Implement WebSockets for real-time push notifications of order status changes from backend to Staff UI (and potentially Customer UI in later phases).
    *   **Customer UI - Basic Menu Display (React):**
        *   Develop a basic customer-facing UI to display the menu (read-only for now).
        *   Fetch menu data from the backend API.
    *   **Refinement of Staff UI:** Enhance Staff UI based on feedback from previous phases, potentially including real-time order status updates in the Staff UI as well.
*   **Tech Stack (Phase 4):** (Building upon previous stacks) + Flask-SocketIO (or similar WebSocket library), WebSocket client in React.
*   **Testing (Phase 4):**
    *   **Real-time Update Testing:** Test the WebSocket implementation for real-time order updates, ensuring messages are correctly sent and received by the Staff UI.
    *   **Customer Menu UI Testing (Basic):** Basic manual testing of the Customer Menu UI to ensure menu items are displayed correctly.
    *   **Integration Testing (Backend & Frontend Real-time):** Integration tests to verify the real-time communication flow between backend and frontend for order updates.
*   **Demo Deliverables (Phase 4):**
    *   Real-time order status updates in Staff UI (and potentially Customer UI).
    *   Basic Customer UI displaying the menu.
    *   Tests for real-time update functionality.

**Phase 5: Customer Ordering & Dummy Payment**

*   **Focus:** Enable customers to place orders through the Customer UI and integrate a dummy payment gateway.
*   **Features:**
    *   **Customer UI - Order Placement:**
        *   Extend the Customer UI to allow customers to select menu items and place orders.
        *   Integrate with backend API to submit customer orders.
    *   **Dummy Payment Gateway Integration (Backend):**
        *   Implement a dummy payment gateway in the backend to simulate payment processing.
        *   API endpoints for initiating and processing dummy payments.
        *   Update order status based on dummy payment success/failure.
    *   **Order Tracking (Customer UI - Basic):** Basic order status display in Customer UI.
*   **Tech Stack (Phase 5):** (Building upon previous stacks) + Dummy Payment Gateway logic in backend.
*   **Testing (Phase 5):**
    *   **Customer Ordering Flow Testing (End-to-End):** End-to-end tests to verify the complete customer ordering flow, from menu browsing to order placement and status updates.
    *   **Dummy Payment Gateway Testing (Integration):** Integration tests for the dummy payment gateway, simulating success and failure scenarios.
    *   **Customer UI Testing (Order Placement):** UI tests for the Customer Order Placement UI components.
*   **Demo Deliverables (Phase 5):**
    *   Customer UI for browsing menu and placing orders.
    *   Dummy payment gateway integration.
    *   Basic order tracking in Customer UI.
    *   End-to-end tests for customer ordering and payment flow.

**Phase 6: Invoice Generation & Table Reservation (Basic)**

*   **Focus:** Implement invoice generation and basic table reservation functionality.
*   **Features:**
    *   **Invoice Generation (Backend):**
        *   Implement backend logic to generate invoices in PDF format upon successful payment.
        *   API endpoint to retrieve invoices.
    *   **Basic Table Reservation (Customer UI & Backend):**
        *   Basic Customer UI for table reservation (selecting date/time and table - very simplified for this phase).
        *   Backend API endpoints for handling table reservations.
    *   **Staff UI - Invoice Viewing:** Staff UI to view and potentially download generated invoices.
*   **Tech Stack (Phase 6):** (Building upon previous stacks) + PDF generation library (ReportLab in Python or similar).
*   **Testing (Phase 6):**
    *   **Invoice Generation Testing (Unit & Integration):** Unit tests for invoice generation logic, integration tests to ensure invoices are correctly generated upon payment and data is accurate.
    *   **Table Reservation Testing (End-to-End):** End-to-end tests for the basic table reservation flow.
    *   **UI Testing (Invoice & Reservation):** UI tests for Customer Reservation UI and Staff Invoice viewing UI.
*   **Demo Deliverables (Phase 6):**
    *   Invoice generation functionality.
    *   Basic Customer Table Reservation feature.
    *   Staff UI for viewing invoices.
    *   Tests for invoice generation and table reservation.

**Phase 7 & Beyond: Enhancements, Loyalty, Feedback, Reporting, Refinements**

*   **Focus:**  In subsequent phases, we can focus on enhancements, more advanced features, and polish:
    *   **Loyalty Program:** Implement loyalty points, rewards, etc.
    *   **Customer Feedback System:**  Implement feedback submission and viewing.
    *   **Reporting & Analytics Dashboard (Staff UI):** Develop a dashboard for sales reports, popular items, etc.
    *   **UI/UX Refinements:** Improve the user interface and user experience based on feedback and testing.
    *   **Security Enhancements:** Implement user authentication, authorization, and security best practices.
    *   **Scalability & Performance Optimizations:**  Address scalability and performance as needed.
