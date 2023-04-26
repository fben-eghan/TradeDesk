from data_analyzer import DataAnalyzer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error


class GasTradingPredictor:
    """
    A class for predicting gas trading performance using ESG metrics.
    """

    def __init__(self, db_file, table_name, numerical_features, categorical_features, target):
        """
        Initializes a GasTradingPredictor object.

        Parameters:
            db_file (str): The name of the database file containing the gas trading data.
            table_name (str): The name of the table containing the gas trading data.
            numerical_features (list of str): The names of the numerical features in the data.
            categorical_features (list of str): The names of the categorical features in the data.
            target (str): The name of the target variable in the data.
        """
        self.analyzer = DataAnalyzer(db_file, table_name)
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.target = target
        self.preprocessing = ColumnTransformer([
            ('num', StandardScaler(), self.numerical_features),
            ('cat', OneHotEncoder(), self.categorical_features)
        ])
        self.rf_model = RandomForestRegressor()
        self.gb_model = GradientBoostingRegressor()
        self.rf_pipeline = Pipeline([
            ('preprocessing', self.preprocessing),
            ('model', self.rf_model)
        ])
        self.gb_pipeline = Pipeline([
            ('preprocessing', self.preprocessing),
            ('model', self.gb_model)
        ])

    def clean_data(self):
        """
        Cleans the gas trading data.
        """
        self.analyzer.clean_data()

    def fit_models(self, param_grid):
        """
        Fits the random forest and gradient boosting models to the data.

        Parameters:
            param_grid (dict): A dictionary of hyperparameters to search over for each model.
        """
        rf_cv = GridSearchCV(self.rf_pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
        rf_cv.fit(self.analyzer.df[self.numerical_features + self.categorical_features], self.analyzer.df[self.target])
        self.rf_best_model = rf_cv.best_estimator_

        gb_cv = GridSearchCV(self.gb_pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
        gb_cv.fit(self.analyzer.df[self.numerical_features + self.categorical_features], self.analyzer.df[self.target])
        self.gb_best_model = gb_cv.best_estimator_

    def evaluate_models(self):
        """
        Evaluates the performance of the random forest and gradient boosting models using cross-validation.
        """
        rf_scores = cross_val_score(self.rf_best_model,
                                    self.analyzer.df[self.numerical_features + self.categorical_features],
                                    self.analyzer.df[self.target],
                                    cv=5,
                                    scoring='neg_mean_squared_error')
        self.rf_rmse = (-rf_scores.mean())**0.5

        gb_scores = cross_val_score(self.gb_best_model,
                                    self.analyzer.df[self.numerical_features + self.categorical_features],
                                    self.analyzer.df[self.target],
                                    cv=5,
                                    scoring='neg_mean_squared_error')
        
        self.gb_rmse = (-gb_scores.mean())**0.5

        
if __name__ == '__main__':
    # Set up database and input variables
    db_file = 'gas_trading_data.db'
    table_name = 'gas_trading_table'
    numerical_features = ['esg_metric_1', 'esg_metric_2', 'non_esg_metric_1', 'non_esg_metric_2']
    categorical_features = ['region', 'industry']
    target = 'gas_trading_performance'

    # Create predictor object and clean the data
    predictor = GasTradingPredictor(db_file, table_name, numerical_features, categorical_features, target)
    predictor.clean_data()

    # Set up parameter grid for grid search
    param_grid = {
        'model__n_estimators': [50, 100, 200],
        'model__max_depth': [5, 10, 20]
    }

    # Fit models using grid search and evaluate their performance
    predictor.fit_models(param_grid)
    predictor.evaluate_models()

    # Print the root mean squared error of the random forest and gradient boosting models
    print(f'Random forest RMSE: {predictor.rf_rmse}')
    print(f'Gradient boosting RMSE: {predictor.gb_rmse}')
