# Workflow in Technical Terms

This document explains the technical workflow of the **Dine-In Manager** application, starting from table reservation to feedback submission. It describes the interactions between the **front-end**, **back-end**, **database**, and **external services**.

---

## **1. Customer Reserves a Table**
- **Front-End:**
  - The customer interacts with the app's UI to select a table and make a reservation.
  - A `POST /reserve` API request is sent to the back-end with details like table ID, customer name, and reservation time.
- **Back-End:**
  - The reservation request is validated (e.g., table availability, valid time slot).
  - The `Tables` table in the database is updated to mark the table as "reserved."
  - A confirmation response is sent back to the front-end, and the customer sees a success message.

---

## **2. Customer Views the Menu and Places an Order**
- **Front-End:**
  - The customer navigates to the menu section, which fetches the latest menu data via a `GET /menu` API call.
  - The customer selects items and submits the order via a `POST /order` API request, including the table ID and selected items.
- **Back-End:**
  - The order is validated (e.g., item availability, table ID validity).
  - A new entry is created in the `Orders` table with status "Pending."
  - The kitchen staff is notified in real-time via WebSocket or a push notification system.
  - A confirmation response is sent to the front-end, and the customer sees the order status as "Pending."

---

## **3. Kitchen Prepares the Order**
- **Back-End:**
  - The kitchen staff updates the order status to "In Progress" via the staff interface (e.g., `PUT /order/{id}`).
  - The `Orders` table is updated with the new status.
  - Real-time updates are pushed to the customer's app using WebSocket or a similar real-time communication protocol.
- **Front-End:**
  - The customer sees the order status change to "In Progress" in real-time.

---

## **4. Order is Ready**
- **Back-End:**
  - Once the kitchen completes the order, the staff updates the status to "Ready" via the staff interface.
  - The `Orders` table is updated, and the customer is notified via WebSocket or push notification.
- **Front-End:**
  - The customer sees the order status change to "Ready."

---

## **5. Customer Tracks the Order**
- **Front-End:**
  - The customer can track the order status in real-time by polling the `GET /order/{id}` API or receiving WebSocket updates.
- **Back-End:**
  - The API fetches the latest order status from the `Orders` table and returns it to the front-end.

---

## **6. Customer Makes a Payment**
- **Front-End:**
  - The customer initiates payment via the app's payment interface.
  - A `POST /payment` API request is sent to the back-end, including the order ID and payment method (e.g., card, digital wallet, cash).
- **Back-End:**
  - The payment request is forwarded to an dummy payment gateway for processing.
  - The payment gateway returns a success or failure response.
  - If successful:
    - The `Payments` table is updated with the payment details.
    - The `Orders` table is updated to mark the order as "Paid."
  - A payment confirmation response is sent to the front-end.

---

## **7. Invoice is Generated**
- **Back-End:**
  - A `GET /invoice/{id}` API request triggers the invoice generation process.
  - A PDF invoice is generated using a library like PDFKit, including order details, payment details, and restaurant information.
  - The invoice is stored in a designated folder (e.g., `/invoices`) and its path is saved in the `Invoices` table.
  - The invoice is sent to the customer via email or made available for download in the app.
- **Front-End:**
  - The customer receives the invoice and can download it as a PDF.

---

## **8. Customer Submits Feedback**
- **Front-End:**
  - The customer submits feedback via the app's feedback interface.
  - A `POST /feedback` API request is sent to the back-end, including the order ID, rating, and comments.
- **Back-End:**
  - The feedback is validated and stored in the `Feedback` table.
  - Loyalty points are calculated and updated in the `Loyalty` table.
  - A confirmation response is sent to the front-end.

---

## **9. Transaction is Completed**
- **Back-End:**
  - The `Tables` table is updated to mark the table as "Available."
  - The order lifecycle is complete, and all relevant data is stored in the database for reporting and analytics.
- **Front-End:**
  - The customer sees a confirmation message and can leave feedback or exit the app.

---
