import pandas as pd


class DataFrameToCSVConverter:
    def __init__(self, dataframe):
        """
        Initialize the converter with a DataFrame.

        :param dataframe: pandas DataFrame to be converted to CSV.
        """
        self.dataframe = dataframe

    def to_csv(self, file_name):
        """
        Convert the DataFrame to a CSV file.

        :param file_name: Name of the CSV file to be created.
        """
        self.dataframe.to_csv(file_name, index=False)
        print(f"DataFrame has been written to {file_name}")


class DataFrameToCSVConverter:
    @staticmethod
    def to_csv(dataframe, file_name):
        """
        Convert the DataFrame to a CSV file.

        :param dataframe: pandas DataFrame to be converted to CSV.
        :param file_name: Name of the CSV file to be created.
        """
        dataframe.to_csv(file_name, index=False)
        print(f"DataFrame has been written to {file_name}")


