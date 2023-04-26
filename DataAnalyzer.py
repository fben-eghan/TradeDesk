import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from scipy import stats

class DataAnalyzer:
    """
    A class that performs data analysis on ESG and non-ESG performance data retrieved from an SQL database.
    """
    
    def __init__(self, database_name, table_name):
        """
        Initializes a new DataAnalyzer object with the specified database name and table name.
        
        Args:
        - database_name (str): the name of the SQL database to connect to
        - table_name (str): the name of the table in the database to retrieve data from
        """
        self.conn = sqlite3.connect(database_name)
        self.table_name = table_name
        self.df = self.retrieve_data()
    
    def retrieve_data(self):
        """
        Retrieves data from the SQL database and returns it as a pandas DataFrame.
        
        Returns:
        - df (pandas DataFrame): the DataFrame containing the retrieved data
        """
        query = f"SELECT * FROM {self.table_name}"
        return pd.read_sql_query(query, self.conn)
    
    def clean_data(self):
        """
        Cleans the data by dropping rows with missing values, dropping duplicate rows, and converting the performance
        value column to numeric.
        """
        self.df = self.df.dropna() # Drop rows with missing values
        self.df = self.df.drop_duplicates() # Drop duplicate rows
        self.df['performance_value'] = pd.to_numeric(self.df['performance_value'], errors='coerce') # Convert to numeric
    
    def analyze_data(self):
        """
        Analyzes the data by computing the mean ESG and non-ESG performance values over time, and performing a t-test
        to determine if there is a statistically significant difference between the two sets of performance values.
        
        Returns:
        - esg_data_by_time (pandas DataFrame): the DataFrame containing the mean ESG performance values by time
        - non_esg_data_by_time (pandas DataFrame): the DataFrame containing the mean non-ESG performance values by time
        - ttest_result (tuple): a tuple containing the t-statistic and p-value from the t-test
        """
        esg_data = self.df[self.df['performance_type'] == 'ESG']
        non_esg_data = self.df[self.df['performance_type'] == 'Non-ESG']
        esg_data_by_time = esg_data.groupby('time').mean()
        non_esg_data_by_time = non_esg_data.groupby('time').mean()
        ttest_result = stats.ttest_ind(esg_data['performance_value'], non_esg_data['performance_value'])
        return esg_data_by_time, non_esg_data_by_time, ttest_result
    
    def visualize_data(self):
        """
        Visualizes the ESG and non-ESG performance values over time using a line plot.
        """
        esg_data_by_time, non_esg_data_by_time, _ = self.analyze_data()
        plt.plot(esg_data_by_time.index, esg_data_by_time['performance_value'], label='ESG')
        plt.plot(non_esg_data_by_time.index, non_esg_data_by_time['performance_value'], label='Non-ESG')
        plt.xlabel('Time')
        plt.ylabel('Performance Value')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    analyzer = DataAnalyzer('mydatabase.db', 'mytable')
    analyzer.clean_data()
    analyzer.visualize_data()
    esg_data_by_time, non_esg_data_by_time, ttest_result = analyzer.analyze_data()
    print('ESG Performance Mean:', esg_data_by_time['performance_value'].mean())
    print('Non-ESG Performance Mean:', non_esg_data_by_time['performance_value'].mean())
    print('T-Test Result:', ttest_result)
