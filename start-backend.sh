#!/bin/bash
cd /home/sonwerik/Develop/apollo/backend

# Instal·la dependències
echo "Sincronitzant dependències..."
uv sync

# Inicia el backend usant directament el Python del venv
echo "Iniciant backend..."
echo "Nota: La primera execució descarregarà el model BERT (~500MB)"
.venv/bin/python -m uvicorn apollo_backend.main:app --reload
