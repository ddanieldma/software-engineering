import time
import random
from vending import *

class VendingMachineSimulator:
    """
    Simulates operations on a VendingMachine instance.

    Methods:
        simulate_stock_changes(machine, iterations=10, delay=2): Simulates random stock changes for a vending machine.
    """

    @staticmethod
    def simulate_stock_changes(machine: VendingMachine, iterations: int = 10, delay: int = 2):
        """
        Simulates random stock changes for a vending machine.

        Args:
            machine (VendingMachine): The vending machine to simulate.
            iterations (int): Number of changes to simulate.
            delay (int): Time (in seconds) between simulations.
        """
        print(f"Starting simulation for Vending Machine {machine.get_id()} at {machine.get_location()}...")

        for _ in range(iterations):
            try:
                # Get all current stock
                stock = machine.get_stock()

                if not stock:
                    print("No products available in this vending machine.")
                    break

                # Randomly select a product and change its stock
                product = random.choice(list(stock.keys()))
                current_quantity = stock[product]
                quantity_change = random.randint(-5, 5)  # Random change between -5 and +5

                new_quantity = max(current_quantity + quantity_change, 0)
                machine.set_stock(product.get_name(), new_quantity)

                print(f"Updated '{product}': {current_quantity} -> {new_quantity}")

            except ValueError as e:
                print(f"Error: {e}")

            # Wait before the next iteration
            time.sleep(delay)

        print("Simulation complete.")

# Exemplo de uso
if __name__ == "__main__":
    # Substitua `1` pelo ID da vending machine que você deseja simular
    vending_machine_id = 3
    machine = VendingMachine(vending_machine_id)

    print("Initial stock:")
    try:
        stock = machine.get_stock()
        for product, quantity in stock.items():
            print(f"{product}: {quantity}")
    except ValueError as e:
        print(f"Error: {e}")

    # Simular mudanças no estoque
    simulator = VendingMachineSimulator()
    simulator.simulate_stock_changes(machine, iterations=5, delay=1)

    print("Final stock:")
    try:
        stock = machine.get_stock()
        for product, quantity in stock.items():
            print(f"{product}: {quantity}")
    except ValueError as e:
        print(f"Error: {e}")