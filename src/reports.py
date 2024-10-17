from database_managment import DBConnection

class ProblemReport:
    """
    Represents a report of a problem.
    """
    def __init__(self, id: int):
        """
        Initializes the ProblemReport instance with the machine's ID and an empty stock cache.
        
        Args:
            id (int): The ID of the problem report.
        """
        self._id: int = id
        self._id_usuario: int | None = None
        self._type: str | None = None
        self._description: str | None = None
        self._status: str | None = None
        self._date_reported: str | None = None
        self._date_solved: str | None = None
        self._id_vending_machine: int | None = None
        
    def get_id(self) -> int:
        """
        Returns the ID of the problem report.
        
        Returns:
            int: The ID of the problem report.
        """
        return self._id

    def load_from_db(self):
        """
        Loads report details from the database.

        Raises:
            ValueError: If the report ID is not found in the database.
        """
        query = f"SELECT * FROM problemas_reportados WHERE id = {self._id}"
        result = DBConnection().execute_query(query, fetch_all=False)

        if result is None:
            raise ValueError(f"Report ID {self._id} not found in the database.")
        
        _, self._id_usuario, self._type, self._description, self._status, self._date_reported, self._date_solved, self._id_vending_machine = result

    def get_user_id(self) -> int:
        """
        Returns the ID of the user that reported the problem.
        
        Returns:
            int: The ID of the user that reported the problem.
        """
        if self._id_usuario is None:
            self.load_from_db()

        return self._id_usuario
    
    def get_type(self) -> str:
        """
        Returns the type of problem reported.
        
        Returns:
            str: The type of problem reported.
        """
        if self._type is None:
            self.load_from_db()

        return self._type
    
    def get_description(self) -> str:
        """
        Returns the description of the problem reported.
        
        Returns:
            str: The description of the problem reported.
        """
        if self._description is None:
            self.load_from_db()

        return self._description
    
    def get_date_reported(self) -> str:
        """
        Returns the date the problem was reported.
        
        Returns:
            str: The date the problem was reported.
        """
        if self._date_reported is None:
            self.load_from_db()

        return self._date_reported
    
    def get_vending_machine_id(self) -> int:
        """
        Returns the ID of the vending machine associated with the problem report.

        Returns:
            int: The ID of the vending machine associated with the problem report.
        """
        if self._id_vending_machine is None:
            self.load_from_db()

        return self._id_vending_machine
    
    def get_status(self) -> str:
        """
        Returns the status of the problem report.
        
        Returns:
            str: The status of the problem report.
        """
        return self._status

    def get_date_solved(self) -> str:
        """
        Returns the date the problem was solved.

        Returns:
            str: The date the problem was solved.
        """
        return self._date_solved