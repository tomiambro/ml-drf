from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

file = Path(settings.APPS_DIR / "ml" / "breast.csv")


class Command(BaseCommand):
    def add_arguments(self, parser):
        return

    def handle(self, *args, **kwargs):
        # read data
        df = pd.read_csv(file)
        df["diagnosis"] = pd.Categorical(df["diagnosis"])
        df["diagnosis"] = df["diagnosis"].cat.codes

        # Feature matrix
        X = df.iloc[:, 2:-1].values

        # Output variable
        y = df.iloc[:, 1]

        # # split test train
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42
        )

        # train model
        estimator = RandomForestClassifier(n_estimators=200)
        estimator.fit(X_train, y_train)

        # Test model
        y_pred = estimator.predict(X_test)

        f1 = f1_score(y_true=y_test, y_pred=y_pred)
        print(f"F1: {f1}")

        # Save Model
        output_path = Path(
            settings.APPS_DIR / "ml/saved_models/randomforest_breast_cancer.pkl"
        )
        joblib.dump(estimator, output_path)
