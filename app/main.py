import os
from dotenv import load_dotenv

from app.services.database.config.handler import DBConnectionHandler

from app.domain.profit_checker import ProfitThresholdChecker
from app.services.binance.client import BinanceClient
from app.services.database.repo.history import HistoryRepository
from app.logs.logger import init_logger

logger = init_logger()

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


def main():
    threshold = 100  # in BRL
    currency = "SOL"
    fiat_pair = "SOLBRL"

    binance_client = BinanceClient(api_key, api_secret)
    with DBConnectionHandler() as db_handler:
        history_repository = HistoryRepository(db_handler)
        profit_checker = ProfitThresholdChecker(binance_client, history_repository)

        if profit_checker.get_initial_balance_in_cents() == 0:
            initial_balance = int(
                input("Type your initial balance in cents for any crypto: ")
            )
            currency = input("Type the currency (e.g., BTC): ")
            history_repository.insert_new_record(
                new_amount=initial_balance, currency=currency
            )

        if profit_checker.get_profit(currency, fiat_pair) >= threshold:
            print("Threshold reached!")
            # TODO: Execute sale logic here


if __name__ == "__main__":
    main()
