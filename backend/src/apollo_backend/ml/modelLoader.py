from transformers import pipeline
from fastapi import HTTPException

# Model multilingüe per anàlisi de sentiments
# Suporta: anglès, català, castellà, francès, alemany, italià, portuguès, etc.
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"

try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )
    MODEL = sentiment_pipeline
except Exception as e:
    print(f"Error carregant model: {e}")
    MODEL = None


def predict_emotion(text: str) -> dict[str, float]:
    """
    Analitza el sentiment d'un text en qualsevol idioma.
    Retorna probabilitats per negative, neutral, positive.
    """
    if MODEL is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Check transformers installation."
        )

    try:
        # El model retorna estrelles (1-5)
        result = MODEL(text[:512])[0]  # Limitar a 512 tokens
        label = result["label"]  # "1 star" a "5 stars"
        score = result["score"]

        # Convertir estrelles a sentiment
        stars = int(label.split()[0])

        # Mapear estrelles a probabilitats
        if stars <= 2:
            # Negatiu
            probs = {
                "0": 0.7 + (score * 0.2),  # negative
                "1": 0.2 - (score * 0.1),  # neutral
                "2": 0.1 - (score * 0.1),  # positive
            }
        elif stars == 3:
            # Neutral
            probs = {
                "0": 0.2,  # negative
                "1": 0.6 + (score * 0.2),  # neutral
                "2": 0.2,  # positive
            }
        else:
            # Positiu (4-5 estrelles)
            probs = {
                "0": 0.1 - (score * 0.05),  # negative
                "1": 0.2 - (score * 0.1),  # neutral
                "2": 0.7 + (score * 0.2),  # positive
            }

        # Normalitzar
        total = sum(probs.values())
        probs = {k: v / total for k, v in probs.items()}

        return probs

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )
