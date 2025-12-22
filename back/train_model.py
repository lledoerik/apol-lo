"""
Script per entrenar el model de sentiment analysis.
Executa: uv run python train_model.py
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

# Paths
DATA_PATH = Path(__file__).parent / "data" / "Pos_Neut_Neg.csv"
MODEL_PATH = Path(__file__).parent / "mlmodel" / "Model.joblib"

def main():
    print("Carregant dades...")

    # Llegir CSV
    df = pd.read_csv(DATA_PATH)

    # Mostrar info del dataset
    print(f"Total mostres: {len(df)}")
    print(f"Columnes: {df.columns.tolist()}")
    print(f"\nDistribucio de classes:")
    print(df['sentiment'].value_counts())

    # Text i labels
    X = df['text'].astype(str)
    y = df['sentiment']

    # Mapear labels a numeros
    label_mapping = {"negative": 0, "neutral": 1, "positive": 2}
    y = y.map(lambda x: label_mapping.get(x.lower().strip(), 1))

    print(f"\nLabels unics: {y.unique()}")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTrain: {len(X_train)}, Test: {len(X_test)}")

    # Pipeline: TF-IDF + Logistic Regression
    print("\nEntrenant model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs', C=1.0))
    ])

    pipeline.fit(X_train, y_train)

    # Avaluacio
    print("\nAvaluacio:")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=['negative', 'neutral', 'positive']))

    # Guardar model
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel guardat a: {MODEL_PATH}")

    # Test rapid
    print("\nTest rapid:")
    test_texts = [
        "I love this, it's amazing!",
        "This is terrible, I hate it",
        "It's okay, nothing special"
    ]
    labels = ['negative', 'neutral', 'positive']
    for text in test_texts:
        pred = pipeline.predict([text])[0]
        proba = pipeline.predict_proba([text])[0]
        print(f"  '{text}' -> {labels[pred]} ({proba[pred]:.1%})")

if __name__ == "__main__":
    main()
