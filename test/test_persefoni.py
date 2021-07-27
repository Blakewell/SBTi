import os
import unittest
from pathlib import Path

import pandas as pd

from SBTi.configs import ColumnsConfig
from SBTi.interfaces import ETimeFrames, EScope
from SBTi.temperature_score import TemperatureScore
from SBTi.portfolio_aggregation import PortfolioAggregationMethod
from SBTi.data.excel import ExcelProvider
from SBTi.portfolio_aggregation import PortfolioAggregationMethod

import SBTi

class TestTemperatureScore(unittest.TestCase):
    """
    Test the reporting functionality. We'll use the Example data provider as the output of this provider is known in
    advance.
    """

    def setUp(self) -> None:

        data_dir_path = Path(os.path.realpath(__file__)).parent.parent.absolute()
        data_path = os.path.join(data_dir_path, "analysis", "data_provider_example.xlsx")

        self.portfolio = pd.read_excel(data_path, sheet_name="portfolio")
        self.provider = ExcelProvider(data_path)
        self.companies = SBTi.utils.dataframe_to_portfolio(self.portfolio)

        time_frames = [ETimeFrames.MID]
        scopes = [EScope.S3]
        fallback_score = 1.5

        self.temperature_score = TemperatureScore(
            time_frames=time_frames,
            scopes=scopes,
            fallback_score=fallback_score,
            aggregation_method=PortfolioAggregationMethod.ROTS 
        )

    def test_temp_score(self) -> None:

        df_scores = self.temperature_score.calculate(data_providers=[self.provider], portfolio=self.companies)
        df_aggregated_scores = self.temperature_score.aggregate_scores(df_scores)

        self.assertEqual(1,1)


if __name__ == "__main__":
    test = TestTemperatureScore()
    test.setUp()
    test.test_temp_score()
    test.test_portfolio_aggregations()
