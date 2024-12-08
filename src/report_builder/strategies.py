from abc import ABC, abstractmethod

class ReportStrategy(ABC):
    @abstractmethod
    def process(self, initial_data):
        """Processa os dados do relatório inicial."""
        pass

import pandas as pd

class AddMetricsStrategy(ReportStrategy):
    def process(self, initial_data):
        # Adiciona métricas ao relatório
        df = pd.DataFrame(initial_data)
        df['new_metric'] = df['value'] * 2  # Exemplo de métrica
        return df

class GroupDataStrategy(ReportStrategy):
    def process(self, initial_data):
        # Agrupa os dados
        df = pd.DataFrame(initial_data)
        grouped = df.groupby('category').sum()
        return grouped.reset_index()

class FilterDataStrategy(ReportStrategy):
    def process(self, initial_data):
        # Filtra os dados
        df = pd.DataFrame(initial_data)
        filtered = df[df['value'] > 10]  # Exemplo de filtro
        return filtered
