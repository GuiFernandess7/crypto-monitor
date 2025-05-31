import logging

logger = logging.getLogger(__name__)
from app.services.binance.client import BinanceClient
from app.services.database.repo.history import HistoryRepository


class ProfitThresholdChecker:
    """
    Checks if the profit from a cryptocurrency exceeds a given threshold.
    """

    def __init__(
        self,
        binance_client: BinanceClient,
        history_repo: HistoryRepository,
        threshold: int = 100,
    ):
        """
        Initialize the checker with Binance client, history repository and threshold.

        :param binance_client: Binance API client instance.
        :param history_repo: Repository to access historical balance data.
        :param threshold: Profit threshold in BRL to compare against.
        """
        self.threshold = threshold
        self.binance_client = binance_client
        self.history_repository = history_repo

    def get_current_balance_in_cents(self, crypto_symbol: str, fiat_symbol: str) -> int:
        """
        Calculate the current balance in cents based on the latest price and holdings.

        :param crypto_symbol: Symbol of the cryptocurrency (e.g., "SOL").
        :param fiat_symbol: Symbol of the fiat pair (e.g., "SOLBRL").
        :return: Current balance in cents.
        """
        total_in_brl = self.binance_client.get_account_total_balance(
            crypto_symbol
        ) * self.binance_client.get_symbol_price(fiat_symbol)
        total_cents = int(round(total_in_brl * 100))
        logger.info(
            f"Current balance of {crypto_symbol} in {fiat_symbol}: R$ {total_cents / 100:.2f}"
        )
        return total_cents

    def get_initial_balance_in_cents(self) -> int:
        """
        Retrieve the most recent recorded balance from the database in cents.

        :return: Previous balance in cents.
        """
        balance_in_cents = self.history_repository.get_balance()
        if balance_in_cents is None:
            logger.error("No balance found in the database.")
            return 0
        logger.info(f"Initial balance: $ {balance_in_cents / 100:.2f}")
        return balance_in_cents

    def get_profit(self, crypto_symbol: str, fiat_symbol: str) -> float:
        """
        Calculate the profit in BRL between current and recorded balances.

        :param crypto_symbol: Symbol of the cryptocurrency.
        :param fiat_symbol: Symbol of the fiat pair.
        :return: Profit in BRL.
        """
        initial = self.get_initial_balance_in_cents()

        if initial == 0:
            logger.warning(
                "Initial balance is zero, cannot calculate profit. Make sure to record the initial balance first."
            )
            return 0.0

        current = self.get_current_balance_in_cents(crypto_symbol, fiat_symbol)
        diff = (current - initial) / 100
        logger.info(f"Difference: $ {diff:.2f}")
        return diff

    def above_threshold(self, crypto_symbol: str, fiat_symbol: str) -> bool:
        """
        Check if the current profit exceeds the configured threshold.

        :param crypto_symbol: Symbol of the cryptocurrency.
        :param fiat_symbol: Symbol of the fiat pair.
        :return: True if profit >= threshold, otherwise False.
        """
        return self.get_profit(crypto_symbol, fiat_symbol) >= self.threshold
