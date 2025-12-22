#!/bin/bash
cd /home/sonwerik/Develop/apollo/frontend

# Carrega nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Usa Node 20
nvm use 20 || nvm install 20

# Instal·la i executa
npm install
npm run dev
