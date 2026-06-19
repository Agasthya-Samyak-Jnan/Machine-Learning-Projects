import numpy as np
def linear_regression_gradient_descent(X: np.ndarray, y: np.ndarray, alpha: float, iterations: int) -> np.ndarray:
	# Your code here, make sure to round
    y = y.reshape(-1,1)
    m, n = X.shape
    theta = np.zeros((n, 1))

    for i in range(iterations) :
        y_pred = X @ theta 
        # loss = np.mean((y - y_pred)**2)
        gradient = (-1/m) * (X.T @ (y - y_pred)) # should be (-2/m) mathematically
        theta -= alpha*gradient

	return theta