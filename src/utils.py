import vending as v
import reports as r
from database_managment import DBConnection

def get_all_vending_machines():
    """
    Retrieves all vending machines available in the database.
    
    Returns:
        list: A list of VendingMachine instances created from the data in the database.
    """
    query = "SELECT id FROM vending_machines"
    result = DBConnection().execute_query(query, fetch_all=True)

    return [v.VendingMachine(id[0]) for id in result]

def get_all_reports():
    """
    Retrieves all reports available in the database.
    
    Returns:
        list: A list of Report instances created from the data in the database.
    """
    query = "SELECT id FROM problemas_reportados"
    result = DBConnection().execute_query(query, fetch_all=True)

    return [r.ProblemReport(id[0]) for id in result]