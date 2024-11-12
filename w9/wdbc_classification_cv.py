import numpy as np
from sklearn import datasets
from sklearn.ensemble import StackingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()

    # Create individual classifiers
    xgb_classifier = XGBClassifier(n_estimators=150, random_state=0)
    logistic_classifier = LogisticRegression(solver='lbfgs', C=0.1)
    multinomial_nb_classifier = MultinomialNB()

    # Define the estimators for the Stacking Classifier
    estimators = [
        ('xgb', xgb_classifier),
        ('logistic', logistic_classifier),
        ('multinomial_nb', multinomial_nb_classifier)
    ]

    # Create a Stacking Classifier with specified estimators
    model = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())

    # Perform cross-validation
    acc_scores = cross_val_score(model, wdbc.data, wdbc.target, cv=5, scoring='accuracy')

    # Evaluate the model
    acc_mean = np.mean(acc_scores)
    acc_test = np.mean(acc_scores)
    print(f'* Accuracy @ training data: {acc_mean:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')
