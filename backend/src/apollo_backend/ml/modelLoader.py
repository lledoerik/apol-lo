import httpx
import os
from fastapi import HTTPException

# Model multilingüe per anàlisi de sentiments via Hugging Face API
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"


def predict_emotion(text: str) -> dict[str, float]:
    """
    Analitza el sentiment d'un text en qualsevol idioma.
    Retorna probabilitats per negative, neutral, positive.
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = httpx.post(
            API_URL,
            headers=headers,
            json={"inputs": text[:512]},
            timeout=30.0
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Hugging Face API error: {response.text}"
            )

        result = response.json()

        # L'API retorna una llista de resultats per cada etiqueta
        # Format: [[{"label": "5 stars", "score": 0.5}, ...]]
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                scores = result[0]
            else:
                scores = result
        else:
            raise HTTPException(
                status_code=500,
                detail="Format de resposta inesperat de l'API"
            )

        # Trobar l'etiqueta amb més puntuació
        best = max(scores, key=lambda x: x["score"])
        label = best["label"]  # "1 star" a "5 stars"
        score = best["score"]

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

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to Hugging Face API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )
