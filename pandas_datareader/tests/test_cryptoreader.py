import pytest

import datetime
import pandas as pd

from pandas_datareader.crypto import CryptoReader
from pandas_datareader.crypto_utils.mapping import extract_mappings
from pandas_datareader.crypto_utils.utilities import yaml_loader


class TestCryptoReader:
    """ Unit tests for the CryptoReader."""

    exchange_name = 'coinbase'
    symbols = 'btc-usd'
    kwargs = {'interval': 'days'}
    CryptoReader = CryptoReader(exchange_name, symbols, **kwargs)

    def test_get_all_exchanges(self):
        """ Test to return a list of all available exchanges."""

        result = self.CryptoReader.get_all_exchanges()

        assert isinstance(result, list)

    def test_read(self):
        """ Test the request from a particular exchange."""

        result = self.CryptoReader.read()

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    def test_request_new_symbol(self):
        """ Test to request NEW symbols."""

        result = self.CryptoReader.read('eth-usd')

        assert 'eth-usd' in self.CryptoReader.symbols.keys()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    def test_extract_mappings(self):
        """ Test to extract the mapping keys and values from the yaml files."""

        result = extract_mappings(self.CryptoReader.name,
                                  self.CryptoReader.yaml_file.get('requests')).get('historic_rates')

        assert isinstance(result, list)
        assert result

    def test_all_exchanges_have_mappings(self):
        """ Test if all exchange yaml-files have a specified mapping."""

        exchanges = self.CryptoReader.get_all_exchanges()
        assert isinstance(exchanges, list)
        assert exchanges

        for exchange in exchanges:
            file = yaml_loader(exchange)
            result = extract_mappings(exchange, file.get('requests')).get('historic_rates')

            assert isinstance(result, list)
            assert result

    def test_necessary_values_in_mappings(self):
        """ Test if all necessary values are in the mappings."""
        # ToDo
        pass

    def test_extract_values_from_response(self):
        """ Tests to correctly extract the values from a specified response."""
        # ToDo
        pass

    def test_iterate_requests_until_no_further_timestamp(self):
        """ Tests to iterate the request with updated timestamps until no more timestamp is collected
            or start time is reached."""
        # ToDo
        pass

    def test_empty_response(self):
        """ Test the behavior for an valid but empty response."""
        # ToDo
        pass

    def test_sort_result_columns(self):
        """ Test to sort the columns of the response."""

        ordered_cols = ['open', 'high', 'low', 'close']
        response = pd.DataFrame({'high': range(0, 5), 'close':  range(0, 5),
                                 'open':  range(0, 5), 'low':  range(0, 5)})
        response = self.CryptoReader._sort_columns(dataframe=response)

        assert all(ordered_cols == response.columns)

    def test_ensure_correct_column_names(self):
        """ Test to ensure specific column names."""

        response = pd.DataFrame({'High': range(0, 5), 'CLOSE':  range(0, 5),
                                 'oPen':  range(0, 5), 'low':  range(0, 5)})
        response = self.CryptoReader._sort_columns(dataframe=response)

        assert response.columns == 'low'

    def test_cut_response_and_set_index(self):
        """ Test to cut the response to the initially defined start/end dates."""

        response = pd.DataFrame({'open': range(0, 100),
                                 'time': pd.period_range(end='2020-12-31', periods=100, freq="d")})

        self.CryptoReader.start = datetime.datetime(2020, 12, 1)
        self.CryptoReader.end = datetime.datetime(2020, 12, 20)

        response = self.CryptoReader._index_and_cut_dataframe(response)

        assert response.shape[0] == 20
        assert min(response.index).to_timestamp() == self.CryptoReader.start
        assert max(response.index).to_timestamp() == self.CryptoReader.end
