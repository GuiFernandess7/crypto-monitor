import logging

logger = logging.getLogger(__name__)
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


class BinanceClient:
    """
    Client to interact with the Binance API to obtain account and market information.
    """

    def __init__(self, api_key: str, api_secret: str):
        """
        Initializes the BinanceClient with the API keys.
        """
        if not api_key or not api_secret:
            logger.error("API key and secret must be provided.")
            raise ValueError("API key and secret must be provided.")
        self._client = self._initialize_client(api_key, api_secret)

    def _initialize_client(self, api_key: str, api_secret: str) -> Client:
        """
        Initializes the Binance API client and synchronizes server time.
        """
        try:
            client = Client(api_key, api_secret, requests_params={"timeout": 10})
            server_time = client.get_server_time()
            Client.TIME_OFFSET = server_time["serverTime"] - int(time.time() * 1000)
            return client
        except (BinanceRequestException, BinanceAPIException) as e:
            logger.error(f"Error initializing Binance client: {e}")
            raise Exception(f"Error initializing Binance client: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during client initialization: {e}")
            raise Exception(f"Unexpected error during client initialization: {e}")

    def get_account_balance(self, asset: str) -> float:
        """
        Returns the FREE balance (available for trading/withdrawal) of an asset.

        Args:
            asset: The asset symbol (e.g., 'SOL', 'BRL').

        Returns:
            The free balance of the asset as a float. Returns 0.0 if not found.
        """
        try:
            account_info = self._client.get_account()
            for balance in account_info.get("balances", []):
                if balance["asset"].upper() == asset.upper():
                    return float(balance["free"])
            return 0.0
        except BinanceAPIException as e:
            logger.error(f"Error getting free balance of {asset}: {e}")
            raise Exception(f"Error getting free balance of {asset}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting free balance of {asset}: {e}")
            raise Exception(f"Unexpected error getting free balance of {asset}: {e}")

    def get_account_total_balance(self, asset: str) -> float:
        """
        Returns the TOTAL balance (free + locked) of an asset in the Spot wallet.

        Args:
            asset: The asset symbol (e.g., 'SOL', 'BRL').

        Returns:
            The total balance of the asset as a float. Returns 0.0 if not found.
        """
        try:
            account_info = self._client.get_account()
            for balance in account_info.get("balances", []):
                if balance["asset"].upper() == asset.upper():
                    return float(balance["free"]) + float(balance["locked"])
            return 0.0
        except BinanceAPIException as e:
            logger.error(f"Error getting TOTAL balance of {asset}: {e}")
            raise Exception(f"Error getting TOTAL balance of {asset}: {e}")
        except Exception as e:
            logger.error(f"Error getting TOTAL balance of {asset}: {e}")
            raise Exception(f"Unexpected error getting TOTAL balance of {asset}: {e}")

    def get_symbol_price(self, symbol: str) -> float:
        """
        Returns the current price of a trading pair (e.g., 'SOLBRL', 'USDTBRL').

        Args:
            symbol: The trading pair symbol.

        Returns:
            The current price of the pair as a float.
        """
        try:
            ticker = self._client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except BinanceAPIException as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            raise Exception(f"Error getting price for {symbol}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting price for {symbol}: {e}")
            raise Exception(f"Unexpected error getting price for {symbol}: {e}")
