import webpage.db as db

class DBConnection:
    """
    Handles connection and interaction with the database.

    Methods:
        get_connection(): Establishes and returns a connection to the database.
        close_connection(): Closes the active database connection.
        execute_query(query, params=None, fetch_all=False): Executes an SQL query on the database, with optional parameters.
        get_all_vending_machines(): Retrieves all available vending machines from the database.
    """
    def __init__(self):
        """Initializes the DBConnection instance."""
        self._connection = None

    def get_connection(self):
        """
        Establishes a connection to the database using the predefined configuration.
        
        Returns:
            mysql.connector.connection.MySQLConnection: The active database connection.
        """
        self._connection = db.get_db_connection()
    
    def close_connection(self):
        """Closes the active database connection."""
        self._connection.close()

    def execute_query(self, query, params=None, fetch_all=False):
        """
        Executes an SQL query on the database, with optional parameters.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): A tuple of parameters to be passed to the SQL query.
            fetch_all (bool, optional): If True, fetches all results; otherwise fetches only the first result. Defaults to False.

        Returns:
            list: A list of the query results. If fetch_all is False, returns only the first result.
        """
        self.get_connection()
        cursor = self._connection.cursor()

        cursor.execute(query, params)
        
        result = cursor.fetchall() if fetch_all else cursor.fetchone()
        
        self.close_connection()
        return result