# Cryptocurrency Monitor

A Python application that monitors cryptocurrency balances and values using the Binance API. The application tracks the value of specified cryptocurrencies against fiat currencies and alerts when predefined thresholds are reached.

## Features

- Real-time cryptocurrency balance monitoring through Binance API
- Support for multiple cryptocurrencies and fiat pairs (e.g., SOL/BRL, BTC/USD)
- Threshold-based profit monitoring
- Historical data storage in SQLite database
- Initial balance tracking and comparison
- Configurable profit thresholds

## Prerequisites

- Python 3.x
- Binance account with API access
- API key and secret from Binance

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cryptobot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Binance API credentials:
```
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```

## Project Structure

```
cryptobot/
├── app/
│   ├── data/           # Database files
│   ├── domain/         # Core business logic
│   ├── errors/         # Custom error handling
│   ├── logs/           # Application logs
│   ├── services/       # External services integration
│   │   ├── binance/    # Binance API integration
│   │   └── postgresql/ # Database operations
│   └── main.py         # Application entry point
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Usage

1. Configure your desired cryptocurrency and threshold in `main.py`:
```python
threshold = 100  # in BRL
currency = "SOL"
fiat_pair = "SOLBRL"
```

2. Run the application:
```bash
python -m app.main
```

3. On first run, you'll be prompted to enter your initial balance in cents for the specified cryptocurrency.

4. The initial balance is stored in a newly created SQLite database file (`.db`) within the `/data` directory. This database serves as a reference point for future value comparisons.

5. The application continuously monitors the current value of your cryptocurrency against the stored initial balance, calculating the profit/loss in real-time.

6. The application will monitor the cryptocurrency value and alert when the threshold is reached.

## Features in Detail

### Balance Monitoring
- Tracks both free and total balances of specified cryptocurrencies
- Supports multiple cryptocurrency pairs
- Real-time price updates through Binance API

### Profit Tracking
- Stores initial balance in SQLite database
- Compares current value against initial investment
- Alerts when profit threshold is reached

### Error Handling
- Comprehensive error handling for API calls
- Logging system for debugging and monitoring
- Graceful handling of network issues

## Security

- API credentials are stored in environment variables
- No hardcoded sensitive information
- Secure API communication through Binance's official client

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational purposes only. Cryptocurrency trading involves risk, and you should never invest more than you can afford to lose.
