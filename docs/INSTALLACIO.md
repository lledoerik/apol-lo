# Guia d'Installacio

Aquest document proporciona instruccions detallades per configurar i executar QuietSignal en un entorn de desenvolupament local.

## Requisits del Sistema

### Software Necessari

| Component | Versio | Notes |
|-----------|--------|-------|
| Node.js | 18+ | Per al frontend |
| Python | 3.10 - 3.13 | Recomanat: 3.11 |
| MySQL | 8.0+ | Base de dades |
| uv | Latest | Gestor de paquets Python |
| Git | Latest | Control de versions |

### Requisits de Hardware

- CPU: Qualsevol processador modern
- RAM: Minim 4 GB
- Disc: Minim 1 GB lliure

## Installacio del Backend

### 1. Navegar al Directori

```bash
cd backend
```

### 2. Installar uv

Si no tens uv installat:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Sincronitzar Dependencies

```bash
uv sync
```

Aixo creara automaticament un entorn virtual i installara totes les dependencies.

### 4. Configurar la Base de Dades

#### Crear la Base de Dades MySQL

```sql
CREATE DATABASE quietsignal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'quietsignal_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON quietsignal.* TO 'quietsignal_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar Variables d'Entorn

Crear un fitxer `.env` al directori `backend/`:

```env
# Configuracio JWT
JWT_SECRET_KEY=clau_secreta_molt_llarga_i_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Configuracio MySQL
MYSQL_USER=quietsignal_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=quietsignal

# Administrador (opcional)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin_password
ADMIN_NAME=Administrator
```

### 6. Verificar el Model ML

Assegurar que el fitxer del model existeix:

```
backend/mlmodel/Model.joblib
```

Si no existeix, cal entrenar el model o obtenir-lo del repositori de dades.

### 7. Executar el Backend

```bash
uv run uvicorn quietsignal_backend.main:app --reload
```

El servidor estara disponible a `http://localhost:8000`.

#### Verificar la Installacio

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/`

## Installacio del Frontend

### 1. Navegar al Directori

```bash
cd frontend
```

### 2. Installar Dependencies

```bash
npm install
```

### 3. Configurar l'Entorn

Crear un fitxer `.env` si cal configurar la URL del backend:

```env
VITE_API_URL=http://localhost:8000
```

### 4. Executar el Frontend

```bash
npm run dev
```

L'aplicacio estara disponible a `http://localhost:5173`.

## Verificacio de la Installacio

### Comprovar el Backend

1. Obrir `http://localhost:8000/docs`
2. Provar l'endpoint GET `/` (health check)
3. Hauria de retornar un missatge d'exit

### Comprovar el Frontend

1. Obrir `http://localhost:5173`
2. Hauria d'apareixer la pagina de login
3. Provar el registre d'un nou usuari

### Provar el Flux Complet

1. Registrar un usuari nou
2. Iniciar sessio
3. Escriure text a l'analitzador
4. Verificar que es retorna un sentiment

## Resolucio de Problemes

### Error de Connexio a MySQL

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
```

Solucio:
- Verificar que MySQL esta en execucio
- Comprovar les credencials al fitxer `.env`
- Assegurar que l'usuari te permisos

### Error del Model ML

```
FileNotFoundError: mlmodel/Model.joblib
```

Solucio:
- Verificar que el fitxer del model existeix
- Descomprimir el fitxer si esta comprimit
- Comprovar els permisos de lectura

### Error de CORS

```
Access-Control-Allow-Origin
```

Solucio:
- Verificar que el backend permet l'origen del frontend
- Comprovar la configuracio CORS a `main.py`

### Port en Us

```
Address already in use
```

Solucio:
- Canviar el port: `uvicorn ... --port 8001`
- Matar el proces que utilitza el port

## Entorns de Desplegament

### Desenvolupament

```bash
# Backend (des del directori backend/)
uv run uvicorn quietsignal_backend.main:app --reload

# Frontend (des del directori frontend/)
npm run dev
```

### Produccio

```bash
# Backend
uv run uvicorn quietsignal_backend.main:app --host 0.0.0.0 --port 8000

# Frontend
npm run build
npm run preview
```

## Scripts Disponibles

### Backend

| Comanda | Descripcio |
|---------|------------|
| `uv sync` | Installar dependencies |
| `uv run uvicorn ...` | Executar servidor |
| `uv run pytest` | Executar tests |

### Frontend

| Comanda | Descripcio |
|---------|------------|
| `npm install` | Installar dependencies |
| `npm run dev` | Servidor de desenvolupament |
| `npm run build` | Compilar per produccio |
| `npm run preview` | Previsualitzar build |
| `npm run lint` | Analitzar codi |
