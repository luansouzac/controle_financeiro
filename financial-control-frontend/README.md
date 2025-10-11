# Financial Control Frontend

This project is a Vue 3 application designed to serve as the frontend for a financial control application. It allows users to manage their financial data, track transactions, and generate reports.

## Project Structure

The project is organized as follows:

```
financial-control-frontend
├── src
│   ├── App.vue                  # Root component of the application
│   ├── main.ts                  # Entry point of the application
│   ├── assets                    # Contains global assets
│   │   ├── base.css             # Global CSS styles
│   │   ├── logo.svg             # Application logo
│   │   └── main.css             # Additional global styles
│   ├── components                # Reusable components
│   │   ├── HelloWorld.vue       # Simple greeting component
│   │   ├── TheWelcome.vue       # Welcome message component
│   │   ├── WelcomeItem.vue      # Individual welcome item component
│   │   ├── FinancialDashboard.vue# Overview of financial data
│   │   ├── TransactionList.vue   # Lists all transactions
│   │   ├── TransactionForm.vue   # Form to add new transactions
│   │   └── icons                # Icon components
│   ├── router                    # Vue Router setup
│   │   └── index.ts             # Defines application routes
│   ├── views                     # View components
│   │   ├── AboutView.vue        # Information about the application
│   │   ├── HomeView.vue         # Landing page
│   │   ├── DashboardView.vue     # Financial dashboard view
│   │   ├── TransactionsView.vue   # Transaction list and form view
│   │   └── ReportsView.vue      # Financial reports view
│   └── store                     # Vuex store setup
│       └── index.ts             # Manages application state
├── package.json                  # npm configuration file
├── tsconfig.json                 # TypeScript configuration file
└── README.md                     # Project documentation
```

## Features

- **Financial Dashboard**: Provides an overview of financial data, including balances and summaries.
- **Transaction Management**: Users can view, add, and manage their transactions.
- **Reports**: Generate financial reports based on user transactions.
- **Responsive Design**: The application is designed to be responsive and user-friendly.

## Installation

To get started with the project, clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd financial-control-frontend
npm install
```

## Usage

To run the application in development mode, use the following command:

```bash
npm run serve
```

The application will be available at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.