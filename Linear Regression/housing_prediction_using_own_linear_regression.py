import numpy as np
from sklearn.datasets import fetch_california_housing
import pandas as pd

class LinearRegression :
    def __init__ (self) :
        self.theta = []

    def fit (self, X, Y) :
        X = np.array(X)
        Y = np.array(Y)
        X_t = np.transpose(X)
        self.theta = np.linalg.inv(X_t @ X) @ (X_t @ Y)
    
    def predict (self, X) :
        X = np.array(X)
        if X.ndim == 1 :
            X = X.reshape(1,-1)
        y = X @ self.theta
        return y
    
def main () :

    housing = fetch_california_housing(as_frame=True)
    X = housing.data
    y = housing.target
    print(y[1])
    
    model = LinearRegression()
    model.fit(X,y)
    print(model.predict(X.iloc[1]))

main()