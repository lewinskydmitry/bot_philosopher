import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

class Module:
    def __init__(self, classifiers):
        self.classifiers = classifiers
        self.number = len(self.classifiers)


    def fit(self, X_train, y_train):
        for clf in self.classifiers:
            clf.fit(X_train, y_train)


    def predict(self, X_test):
        y_preds = []

        for clf in self.classifiers:
            y_preds.append(clf.predict(X_test))

        y_preds = np.stack(y_preds)

        # Most popular guess for each item. +0.5 because numpy can't round properly
        return np.floor(y_preds.sum(axis=0) / self.number + 0.5).astype(int) 


if __name__ == "__main__":
    """
    1. Load iris dataset
    2. Shuffle data and divide into train / test.
    3. Prepare classifiers to initialize <StructuralPatternName> class.
    4. Train the ensemble
    """
    train_size = 0.7

    X, y = load_iris(return_X_y=True)
    X, y = shuffle(X, y, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=42)

    classifiers = [SVC(),
                   RandomForestClassifier(),
                   KNeighborsClassifier(7)]

    classifiers_gr = Module(classifiers)

    classifiers_gr.fit(X_train, y_train)

    y_pred = classifiers_gr.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy score achieved with ensemble = {accuracy}")