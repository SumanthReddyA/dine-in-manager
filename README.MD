# Dine-In Manager Backend - Phase 1

## Setup Instructions

To run the Dine-In Manager backend application, please follow these steps:

1.  **Prerequisites:**
    *   **PostgreSQL:** Ensure you have PostgreSQL installed and running. You will need a PostgreSQL database server to store the application data.
    *   **Python:** Make sure you have Python installed on your system. This project is built using Python.

2.  **Environment Variables:**
    *   **`POSTGRES_PASSWORD`:**  You need to set an environment variable named `POSTGRES_PASSWORD` that contains the password for your PostgreSQL `postgres` user (or whichever user you intend to use).
        *   **On Windows:** You can set this using the `setx` command in the command prompt (run as administrator):
            ```bash
            setx POSTGRES_PASSWORD "your_postgres_password"
            ```
            **(Replace `"your_postgres_password"` with your actual PostgreSQL password).**
            *   Remember to restart your terminal or VS Code after setting the environment variable for it to take effect in new processes.

3.  **Install Python Dependencies:**
    *   Navigate to the project's root directory (`dine-in-manager`) in your terminal.
    *   Run the following command to install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **(Optional) Database URI Configuration:**
    *   For Phase 1, we are using a simplified database configuration that reads only the password from the `POSTGRES_PASSWORD` environment variable and assumes a local PostgreSQL server with the default `postgres` user and a database named `dine_in_db`.
    *   In `backend/src/app.py`, if you need to customize the full database URI (e.g., to use a different username, host, port, or database name), you can modify the `SQLALCHEMY_DATABASE_URI` configuration in the Flask app.  For more advanced setups, consider setting the entire database URI in the `DATABASE_URL` environment variable instead of just the password.

5.  **Run the Flask Application:**
    *   Navigate to the `backend/src` directory in your terminal:
        ```bash
        cd backend/src
        ```
    *   Run the Flask application using:
        ```bash
        python app.py
