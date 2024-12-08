from report_builder.strategies import ReportStrategy

class ReportGenerator:
    def __init__(self, strategy: ReportStrategy = None):
        # Strategy can be optionally provided during initialization
        self.strategy = strategy

    def set_strategy(self, strategy: ReportStrategy):
        # This method allows setting the strategy after initialization
        self.strategy = strategy

    def generate_report(self, initial_data):
        # Only needs initial_data now; strategy is already set
        if not self.strategy:
            raise ValueError("Strategy not set.")
        return self.strategy.process(initial_data)

