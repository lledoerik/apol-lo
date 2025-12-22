"""
Script per re-entrenar el model amb el feedback dels usuaris.
Executa: uv run python retrain_with_feedback.py

Això combina:
1. El dataset original (Pos_Neut_Neg.csv)
2. El feedback dels usuaris (de la BD)

Les correccions dels usuaris tenen més pes per prioritzar el que han dit.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from pathlib import Path
import requests
from datetime import datetime

# Paths
DATA_PATH = Path(__file__).parent / "data" / "Pos_Neut_Neg.csv"
MODEL_PATH = Path(__file__).parent / "mlmodel" / "Model.joblib"
BACKUP_PATH = Path(__file__).parent / "mlmodel" / "backups"

# API per obtenir feedback
FEEDBACK_API = "http://localhost:8000/feedback/export"


def get_feedback_data():
    """Obté les dades de feedback de l'API"""
    try:
        response = requests.get(FEEDBACK_API)
        data = response.json()

        if data.get("success") and data.get("data"):
            return data["data"]
        return []
    except Exception as e:
        print(f"Error obtenint feedback: {e}")
        return []


def main():
    print("=" * 50)
    print("Re-entrenament del model amb feedback")
    print("=" * 50)

    # 1. Carregar dataset original
    print("\n1. Carregant dataset original...")
    df_original = pd.read_csv(DATA_PATH)
    print(f"   - {len(df_original)} mostres originals")

    # 2. Obtenir feedback dels usuaris
    print("\n2. Obtenint feedback dels usuaris...")
    feedback_data = get_feedback_data()
    print(f"   - {len(feedback_data)} mostres de feedback")

    if len(feedback_data) == 0:
        print("\n   No hi ha feedback disponible. Usant només dataset original.")
        df_feedback = pd.DataFrame(columns=['text', 'sentiment'])
    else:
        # Convertir a DataFrame
        df_feedback = pd.DataFrame(feedback_data)
        df_feedback = df_feedback[['text', 'sentiment']]

        # Les correccions dels usuaris es dupliquen per donar-los més pes
        # Això fa que el model aprengui més d'aquestes mostres
        print("   - Duplicant correccions per donar-los més pes...")
        df_feedback = pd.concat([df_feedback] * 3, ignore_index=True)
        print(f"   - {len(df_feedback)} mostres de feedback (amb pes)")

    # 3. Combinar datasets
    print("\n3. Combinant datasets...")
    df_combined = pd.concat([df_original, df_feedback], ignore_index=True)
    print(f"   - Total: {len(df_combined)} mostres")

    # Mostrar distribució
    print(f"\n   Distribució de classes:")
    print(df_combined['sentiment'].value_counts())

    # 4. Preparar dades
    print("\n4. Preparant dades...")
    X = df_combined['text'].astype(str)
    y = df_combined['sentiment']

    # Mapear labels a números
    label_mapping = {"negative": 0, "neutral": 1, "positive": 2}
    y = y.map(lambda x: label_mapping.get(str(x).lower().strip(), 1))

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   - Train: {len(X_train)}, Test: {len(X_test)}")

    # 5. Backup del model anterior
    print("\n5. Fent backup del model anterior...")
    if MODEL_PATH.exists():
        BACKUP_PATH.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_PATH / f"Model_{timestamp}.joblib"
        import shutil
        shutil.copy(MODEL_PATH, backup_file)
        print(f"   - Backup guardat a: {backup_file}")
    else:
        print("   - No hi ha model anterior per fer backup")

    # 6. Entrenar nou model
    print("\n6. Entrenant nou model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs', C=1.0))
    ])

    pipeline.fit(X_train, y_train)

    # 7. Avaluació
    print("\n7. Avaluació del nou model:")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=['negative', 'neutral', 'positive']))

    # 8. Guardar model
    print("\n8. Guardant nou model...")
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"   - Model guardat a: {MODEL_PATH}")

    # 9. Test ràpid
    print("\n9. Test ràpid:")
    test_texts = [
        "Estic molt content avui!",
        "Ha sigut un dia horrible",
        "Normal, res especial",
        "Me siento muy feliz",
        "I feel great today!"
    ]
    labels = ['negative', 'neutral', 'positive']
    for text in test_texts:
        pred = pipeline.predict([text])[0]
        proba = pipeline.predict_proba([text])[0]
        print(f"   '{text}' -> {labels[pred]} ({proba[pred]:.1%})")

    print("\n" + "=" * 50)
    print("Re-entrenament completat!")
    print("=" * 50)


if __name__ == "__main__":
    main()
