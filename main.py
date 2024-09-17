import pickle
import numpy as np
import nltk
#nltk.download()
#nltk.download('punkt')
#nltk.download("stopwords")
from abc import ABC, abstractmethod
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        pass


class NLTKTagger(BaseTagger):
    def __init__(self, classification_threshold=0.2, filename_with_weights="model_weights.pik"):

        self.classification_threshold = classification_threshold
        self.classifier = Pipeline(
            [('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
            ('clf_svm', SGDClassifier(learning_rate='adaptive', eta0=0.1, loss='modified_huber', penalty='elasticnet',
                                      tol=1e-5, alpha=1e-5, max_iter=50, early_stopping=True, random_state=42))])

        twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
        self.targets = twenty_test.target_names

        try:
            self.classifier = pickle.load(open(filename_with_weights, 'rb'))
            print("The model fitted from pre-saved weights")

        except FileNotFoundError as error:
            print("The model needs fitting as no pre-fitted weights are available")
            twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

            self.classifier = self.classifier.fit(twenty_train.data, twenty_train.target)
            predictions = self.classifier.predict(twenty_test.data)
            print(f"Model accuracy:{np.mean(predictions == twenty_test.target):.2f}")

            pickle.dump(self.classifier, open(filename_with_weights, 'wb'))

    def get_tags(self, texts: list[str]) -> list[list[str]]:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        tags = []
        tag_scores = []
        for text in texts:
            predictions = self.classifier.predict_proba([text])[0].tolist()
            sorted_scores = [(predictions[i], predictions.index(predictions[i])) for i in range(len(predictions))]
            sorted_scores = sorted(sorted_scores, reverse=True, key=lambda x: x[0])
            valid_predictions = []
            valid_predictions_scores = []

            for v in range(len(sorted_scores)):
                if sorted_scores[v][0] >= self.classification_threshold:
                    valid_predictions.append(self.targets[sorted_scores[v][1]])
                    valid_predictions_scores.append(sorted_scores[v][0])
            tags.append(valid_predictions)
            tag_scores.append(valid_predictions_scores)

        return tags, tag_scores


texts = [
    "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from noisy, structured and unstructured data",
    "Data science is a concept to unify statistics, data analysis, informatics, and their related methods in order to understand and analyse actual phenomena with data",
    "Data science is an interdisciplinary field focused on extracting knowledge from data sets, which are typically large (see big data), and applying the knowledge and actionable insights from data to solve problems in a wide range of application domains",
    "Hi man! How are you?",
    'Many statisticians, including Nate Silver, have argued that data science is not a new field, but rather another name for statistics'
]

tagger = NLTKTagger()
tags, scores = tagger.get_tags(texts)

print("Tagger predictions:\n", tags)
print(scores)
