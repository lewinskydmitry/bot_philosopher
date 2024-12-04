import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

class Builder:
    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def get_subsample(self, df_share):
        X_train_sample = self.X_train.copy().sample(df_share, random_state=42)
        y_train_sample = self.y_train.copy().sample(df_share, random_state=42)

        return X_train_sample, y_train_sample

if __name__ == "__main__":
    """
    1. Load iris dataset
    2. Shuffle data and divide into train / test.
    """
    X, y = load_iris(return_X_y=True)
    X,y = pd.DataFrame(X),pd.DataFrame(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
    svm = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    pattern_item = Builder(X_train, y_train)
    for df_share in range(10, 101, 10):
        curr_X_train, curr_y_train = pattern_item.get_subsample(df_share)

        svm.fit(curr_X_train, curr_y_train)

        y_pred = svm.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        print(f"df_share = {df_share}%, accuracy on test = {accuracy}")

        """
        1. Preprocess curr_X_train, curr_y_train in the way you want
        2. Train Linear Regression on the subsample
        3. Save or print the score to check how df_share affects the quality
        """