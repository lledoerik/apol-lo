#!/bin/bash
cd /home/sonwerik/Develop/aurora-minds/backend

# Instal·la dependències
echo "Sincronitzant dependències..."
uv sync

# Inicia el backend (el model multilingüe es descarrega automàticament)
echo "Iniciant backend..."
echo "Nota: La primera execució descarregarà el model BERT (~500MB)"
uv run uvicorn quietsignal_backend.main:app --reload
