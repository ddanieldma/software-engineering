from models import *
import reports as r
from database_managment import DBConnection

def get_all_vending_machines():
    """
    Retrieves all vending machines available in the database.
    
    Returns:
        list: A list of VendingMachine instances created from the data in the database.
    """

    return VendingMachine.query.all()

def get_all_reports():
    """
    Retrieves all reports available in the database.
    
    Returns:
        list: A list of Report instances created from the data in the database.
    """

    return ReportedProblem.query.all()