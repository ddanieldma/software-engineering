import threading
import webpage.db as db

class DBConnection:
    """
    Handles connection and interaction with the database, following the Singleton pattern.

    Methods:
        get_connection(): Establishes and returns a connection to the database.
        close_connection(): Closes the active database connection.
        execute_query(query, params=None, fetch_all=False): Executes an SQL query on the database, with optional parameters.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the class is created (thread-safe).
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the DBConnection instance, ensuring the connection is not reinitialized if already exists.
        """
        if not hasattr(self, '_connection'):
            self._connection = None

    def get_connection(self):
        """
        Establishes a connection to the database using the predefined configuration.

        Returns:
            mysql.connector.connection.MySQLConnection: The active database connection.
        """
        if not self._connection:
            self._connection = db.get_db_connection()
        return self._connection

    def close_connection(self):
        """
        Closes the active database connection and resets the connection instance.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query, params=None, fetch_all=False):
        """
        Executes an SQL query on the database, with optional parameters.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): A tuple of parameters to be passed to the SQL query.
            fetch_all (bool, optional): If True, fetches all results; otherwise fetches only the first result. Defaults to False.

        Returns:
            list or tuple: A list of query results if fetch_all is True, otherwise the first result.
        """
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)

        result = cursor.fetchall() if fetch_all else cursor.fetchone()

        # Explicitly close the cursor but keep the connection open for further use
        cursor.close()
        return result
    
    def __del__(self):
        """
        Ensures the database connection is closed when the instance is deleted.
        """
        self.close_connection()
