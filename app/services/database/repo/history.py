import logging

logger = logging.getLogger(__name__)

from datetime import datetime, timezone
from app.services.database.models.history import History
from sqlalchemy import text


class HistoryRepository:
    """
    Manages access to historical cryptocurrency balance records in the database.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session or handler.

        :param db: Database session or connection handler.
        """
        self.db_handler = db

    def insert_new_record(self, new_amount, currency, created_at=None):
        """
        Insert a new historical balance record into the database.

        :param new_amount: The balance amount in cents.
        :param currency: The currency symbol (e.g., 'SOL').
        :param created_at: Optional datetime of the record; uses current UTC if None.
        """
        if created_at is None:
            created_at = datetime.now(timezone.utc)

        new_record = History(
            current_balance=new_amount, currency=currency, created_at=created_at
        )
        try:
            self.db_handler.add(new_record)
            self.db_handler.commit()
        except Exception as e:
            logger.error(f"Error inserting new record: {e}")
            self.db_handler.rollback()
            raise e

    def get_balance(self):
        """
        Retrieve the most recent balance from the history table.

        :return: The last recorded balance in cents.
        :raises ValueError: If no records are found.
        :raises Exception: If a database error occurs.
        """
        query = """
            SELECT current_balance FROM crypto_history
            ORDER BY created_at DESC
            LIMIT 1;
        """
        try:
            result = self.db_handler.execute(text(query))
            row = result.fetchone()
            return row[0] if row else 0.0
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            raise e
