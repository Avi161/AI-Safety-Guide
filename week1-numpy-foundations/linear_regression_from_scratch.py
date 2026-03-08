"""
Linear Regression from Scratch
==============================
Implement a complete linear regression model using only NumPy.

Fill in the TODO sections to complete the implementation.
Then import this module in 05_linear_regression.ipynb to use it.
"""

import numpy as np


class LinearRegressionScratch:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.loss_history = []

    def _compute_cost(self, X, y):
        """
        Compute Mean Squared Error cost.

        Cost = (1 / 2n) * sum((y_pred - y)^2)

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
        y : np.ndarray, shape (n_samples,)

        Returns
        -------
        cost : float
        """
        n_samples = X.shape[0]
        y_pred = X @ self.weights + self.bias

        # TODO: Compute MSE cost
        # cost = ...
        raise NotImplementedError("Implement _compute_cost")

        return cost

    def _compute_gradients(self, X, y):
        """
        Compute gradients of the cost with respect to weights and bias.

        dW = (1/n) * X^T @ (y_pred - y)
        db = (1/n) * sum(y_pred - y)

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
        y : np.ndarray, shape (n_samples,)

        Returns
        -------
        dw : np.ndarray, shape (n_features,)
        db : float
        """
        n_samples = X.shape[0]
        y_pred = X @ self.weights + self.bias
        error = y_pred - y

        # TODO: Compute gradients
        # dw = ...
        # db = ...
        raise NotImplementedError("Implement _compute_gradients")

        return dw, db

    def fit(self, X, y):
        """
        Train the model using gradient descent.

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
        y : np.ndarray, shape (n_samples,)

        Returns
        -------
        self
        """
        n_samples, n_features = X.shape

        # Initialize weights and bias to zeros
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.loss_history = []

        for i in range(self.n_iterations):
            # TODO: 1) Compute gradients
            # TODO: 2) Update weights and bias using gradient descent
            # TODO: 3) Compute and store the cost
            raise NotImplementedError("Implement the training loop in fit()")

        return self

    def predict(self, X):
        """
        Make predictions.

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray, shape (n_samples,)
        """
        # TODO: Compute predictions
        # y_pred = ...
        raise NotImplementedError("Implement predict")

        return y_pred

    def r_squared(self, X, y):
        """
        Compute R-squared (coefficient of determination).

        R^2 = 1 - SS_res / SS_tot
        where SS_res = sum((y - y_pred)^2)
              SS_tot = sum((y - y_mean)^2)

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
        y : np.ndarray, shape (n_samples,)

        Returns
        -------
        r2 : float
        """
        y_pred = self.predict(X)

        # TODO: Compute R-squared
        # ss_res = ...
        # ss_tot = ...
        # r2 = ...
        raise NotImplementedError("Implement r_squared")

        return r2
