from strategies import ReportStrategy

class ReportGenerator:
    def __init__(self, strategy: ReportStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ReportStrategy):
        self.strategy = strategy

    def generate_report(self, initial_data):
        return self.strategy.process(initial_data)
