from abc import ABC, abstractmethod

class ReportStrategy(ABC):
    @abstractmethod
    def process(self, initial_data):
        """Processa os dados do relatório inicial."""
        pass

import pandas as pd
import json
from report_builder.strategies import ReportStrategy
from database_managment import DBConnection

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch MySQL credentials from environment variables
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

def get_db_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="coffe_map"
    )


class VendingMachineReportStrategy(ReportStrategy):
    def process(self, initial_data):
        """
        This method will query the database for vending machine data,
        calculate the revenue, and return the processed results.
        """

        try:
            # Step 1: Establish database connection and create a cursor
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Using dictionary cursor for easier access to results

            # Step 2: Query for vending machine data (revenue and average ratings)
            cursor.execute("""
                SELECT v.id AS machine_id, 
                       v.localizacao, 
                       SUM(p.preco * p.estoque) AS revenue,
                       AVG(a.nota_maquina) AS avg_rating
                FROM vending_machines v
                LEFT JOIN produtos p ON v.id = p.id_vending_machine
                LEFT JOIN avaliacoes a ON v.id = a.id_maquina
                GROUP BY v.id
            """)

            # Fetch the results of the query
            report_data = cursor.fetchall()

            # Log the retrieved data (just for debugging)

            # Step 3: Convert results into a DataFrame for further processing or CSV export
            import pandas as pd
            df = pd.DataFrame(report_data)

            # Step 4: Fetch stock data (machine-wise product stock)
            cursor.execute("""
                SELECT v.id AS machine_id, 
                       p.nome AS product_name, 
                       p.estoque AS stock
                FROM vending_machines v
                JOIN produtos p ON v.id = p.id_vending_machine
                ORDER BY v.id, p.nome
            """)

            # Fetch stock data
            stock_data = cursor.fetchall()
            stock_df = pd.DataFrame(stock_data)

            # Prepare stock data for CSV and JSON format
            stock_pivot = stock_df.pivot_table(index='product_name', columns='machine_id', values='stock', aggfunc='sum', fill_value=0)

            # Step 5: Prepare CSV and JSON data
            revenue_and_rating_csv = df.to_csv(index=False)
            stock_csv = stock_pivot.to_csv()
            stock_json = stock_pivot.to_json(orient="split")

            # Return the final processed data
            return {
                "revenue_and_rating": df,
                "stock_csv": stock_csv,
                "stock_json": stock_json
            }

        except mysql.connector.Error as err:
            return {"error": str(err)}

        finally:
            # Make sure to close the cursor and connection
            cursor.close()
            conn.close()


