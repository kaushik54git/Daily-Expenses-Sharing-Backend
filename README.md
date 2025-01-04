# Daily Expenses Sharing Application

## Objective
This project is a backend service for a daily expenses sharing application. It allows users to add expenses and split them using three different methods: exact amounts, percentages, and equal splits. The application manages user details, validates inputs, and generates downloadable balance sheets.

## Technology Stack
- **Backend Framework**: Flask
- **Database**: MongoDB
- **Authentication**: Flask-JWT-Extended
- **Validation**: Marshmallow
- **File Generation**: ReportLab

## Features
- User Management:
  - Create user
  - Retrieve user details
- Expense Management:
  - Add expense
  - Retrieve individual user expenses
  - Retrieve overall expenses
  - Download balance sheet

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- MongoDB

### Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/kaushik54git/Daily-Expenses-Sharing-Backend.git
    cd Daily Expenses Sharing Backend
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB**
    - Ensure MongoDB is installed and running on your local machine.
    - Create a database named `daily_expenses`.

5. **Configure the application**
    - Edit the `config.py` file if necessary to match your MongoDB URI and other settings.

### Running the Application

1. **Start the Flask application**
    ```bash
    python run.py
    ```

2. **Access the application**
    - The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

### User Endpoints
- **Create User**
  - **URL**: `/users`
  - **Method**: `POST`
  - **Payload**: `{"email": "kaushikkumbhat54@gmail.com", "name": "Kaushik Kumbhat", "mobile": "1234567890"}`
  - **Response**: `{"message": "User created successfully"}`

- **Retrieve User Details**
  - **URL**: `/users/<email>`
  - **Method**: `GET`
  - **Headers**: `Authorization: Bearer <JWT Token>`
  - **Response**: `{"email": "kaushikkumbhat54@gmail.com", "name": "Kaushik Kumbhat", "mobile": "1234567890"}`

### Expense Endpoints
- **Add Expense**
  - **URL**: `/expenses`
  - **Method**: `POST`
  - **Headers**: `Authorization: Bearer <JWT Token>`
  - **Payload**: 
    ```json
    {
      "description": "Dinner",
      "amount": 3000,
      "method": "equal",
      "splits": [
        {"email": "user1@example.com"},
        {"email": "user2@example.com"},
        {"email": "user3@example.com"}
      ]
    }
    ```
  - **Response**: `{"message": "Expense added successfully"}`

- **Retrieve Individual User Expenses**
  - **URL**: `/expenses/user/<email>`
  - **Method**: `GET`
  - **Headers**: `Authorization: Bearer <JWT Token>`
  - **Response**: List of expenses for the specified user.

- **Retrieve Overall Expenses**
  - **URL**: `/expenses`
  - **Method**: `GET`
  - **Headers**: `Authorization: Bearer <JWT Token>`
  - **Response**: List of all expenses.

- **Download Balance Sheet**
  - **URL**: `/balance-sheet`
  - **Method**: `GET`
  - **Headers**: `Authorization: Bearer <JWT Token>`
  - **Response**: PDF file of the balance sheet.

## Validation
- User input is validated using Marshmallow.
- The percentage split method ensures that the percentages add up to 100%.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
