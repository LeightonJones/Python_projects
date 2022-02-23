import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class CustomLinearRegression:
    """Fit a simple regression to data in a DataFrame"""

    def __init__(self, *, fit_intercept=True):

        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None
        self.lin_array = None
        self.return_dict = None

    def fit(self, X, y):
        """Calculates the coefficients and intercept based on x and y values"""

        # Add ones to X array based on whether fit intercept is True
        if self.fit_intercept:
            # Add column of 1's to array
            X = self.add_ones(X)

            self.lin_array = np.linalg.inv(X.T @ X) @ X.T @ y
            self.intercept = self.lin_array[0]
            self.coefficient = self.lin_array[1:]

            self.return_dict = {'Intercept': self.intercept,
                                'Coefficient': self.coefficient}

        else:
            self.coefficient = np.linalg.inv(X.T @ X) @ X.T @ y

            self.return_dict = {'Coefficient': self.coefficient}

    def predict(self, X):
        """Uses coefficient array to predict against new independent
        variables"""

        # Add ones to X array based on whether fit intercept is True
        if self.fit_intercept:
            # Add column of 1's to array
            X = self.add_ones(X)

            return X @ self.lin_array

        else:
            return X @ self.coefficient

    def r2_score(self, y, yhat):
        r2_num = np.sum((y - yhat) ** 2)
        r2_den = np.sum((y - y.mean()) ** 2)

        self.return_dict['R2'] = 1 - (r2_num / r2_den)

    def rmse(self, y, yhat):
        mse = (1/y.shape[0]) * np.sum((y - yhat) ** 2)
        rmse = np.sqrt(mse)
        self.return_dict['RMSE'] = rmse

    @staticmethod
    def add_ones(target_array):
        """Adds a column filled with 1 to the specified array"""
        x1 = np.ones((target_array.shape[0], 1))
        new_array = np.concatenate((x1, target_array), axis=1)

        return new_array


def main():
    df = pd.read_csv('data_stage4.csv')

    # Prepare CustomLinearRegression results
    model = CustomLinearRegression()
    model.fit(df.iloc[:, 0:-1].values, df.iloc[:, -1].values)
    yhat = model.predict(df.iloc[:, 0:-1].values)
    model.r2_score(df.iloc[:, -1].values, yhat)
    model.rmse(df.iloc[:, -1].values, yhat)

    # Prepare sklearn comparison results
    sk_model = LinearRegression()
    sk_model.fit(df.iloc[:, 0:-1].values, df.iloc[:, -1].values)
    sk_yhat = sk_model.predict(df.iloc[:, 0:-1].values)
    sk_r2 = r2_score(df.iloc[:, -1].values, sk_yhat)
    sk_rmse = np.sqrt(mean_squared_error(df.iloc[:, -1].values, sk_yhat))
    sk_dict = {'Intercept': sk_model.intercept_, 'Coefficient': sk_model.coef_,
               'R2': sk_r2, 'RMSE': sk_rmse}

    # Compile difference dictionary
    diff_dict = {'Intercept': model.return_dict['Intercept'] -
                              sk_dict['Intercept'],
                 'Coefficient': model.return_dict['Coefficient'] -
                              sk_dict['Coefficient'],
                 'R2': model.return_dict['R2'] - sk_dict['R2'],
                 'RMSE': model.return_dict['RMSE'] - sk_dict['RMSE']}

    print(diff_dict)


if __name__ == '__main__':
    main()
