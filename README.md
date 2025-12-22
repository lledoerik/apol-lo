# Apol·lo

Diari Emocional

## Descripció

Apol·lo és un projecte centrat en la salut mental i emocional, que identifica l'estat emocional de l'usuari a partir de text mitjançant models avançats de xarxes neuronals.

El sistema permet als usuaris crear diaris personals, escriure entrades i obtenir anàlisis automàtiques del sentiment emocional del seu contingut.

## Característiques

- Autenticació segura amb JWT
- Gestió de diaris i entrades
- Anàlisi de sentiments en temps real (positiu, neutral, negatiu)
- Control d'accés basat en rols
- API RESTful documentada amb OpenAPI

## Stack Tecnològic

### Frontend

| Tecnologia | Versió | Descripció |
|------------|--------|------------|
| React | 19.x | Biblioteca UI |
| Vite | 7.x | Build tool |
| React Router | 7.x | Routing |
| Axios | 1.x | Client HTTP |
| Tailwind CSS | 3.x | Framework CSS |

### Backend

| Tecnologia | Versió | Descripció |
|------------|--------|------------|
| FastAPI | Latest | Framework web |
| Python | 3.13+ | Llenguatge |
| SQLAlchemy | Latest | ORM |
| MySQL | 8.0+ | Base de dades |
| scikit-learn | Latest | Machine Learning |
| PyJWT | Latest | Autenticació |

## Estructura del Projecte

```
apollo/
    frontend/
        src/
            api/
            components/
            pages/
            styles/
        public/
        package.json
    backend/
        src/apollo_backend/
            api/
            services/
            models/
            database/
            ml/
        mlmodel/
        pyproject.toml
    docs/
        API.md
        ARQUITECTURA.md
        DIAGRAMES.md
        DISSENY_UI.md
        INSTALLACIO.md
        MODEL_DADES.md
    README.md
```

## Instal·lació

### Requisits

- Node.js 18+
- Python 3.13+
- MySQL 8.0+
- uv (gestor de paquets Python)

### Backend

```bash
cd backend
uv sync
```

Crear fitxer `.env`:

```env
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=apollo
```

Executar:

```bash
./start-backend.sh
```

### Frontend

```bash
./start-frontend.sh
```

## Documentació

| Document | Descripció |
|----------|------------|
| [API](docs/API.md) | Referència completa dels endpoints |
| [Arquitectura](docs/ARQUITECTURA.md) | Estructura i patrons del sistema |
| [Diagrames](docs/DIAGRAMES.md) | Diagrames UML, ER i wireframes |
| [Disseny UI](docs/DISSENY_UI.md) | Especificacions de la interfície |
| [Instal·lació](docs/INSTALLACIO.md) | Guia detallada de configuració |
| [Model de Dades](docs/MODEL_DADES.md) | Esquema de la base de dades |

## API Endpoints

| Mètode | Ruta | Descripció |
|--------|------|------------|
| POST | /auth/register | Registre d'usuari |
| POST | /auth/login | Autenticació |
| POST | /auth/logout | Tancar sessió |
| GET | /auth/me | Usuari actual |
| POST | /analyze | Analitzar sentiment |
| GET | /journals | Llistar diaris |
| POST | /journals | Crear diari |
| POST | /journals/{id}/entries | Crear entrada |
| GET | /journals/{id}/entries | Llistar entrades |

## Autors

- Alvaro Silva
- Marcel JG
