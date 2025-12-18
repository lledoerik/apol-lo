# Documentacio de l'API

Aquest document descriu tots els endpoints disponibles a l'API de QuietSignal.

## Informacio General

| Propietat | Valor |
|-----------|-------|
| Base URL | `http://localhost:8000` |
| Format | JSON |
| Autenticacio | JWT Bearer Token |

## Autenticacio

L'API utilitza tokens JWT per a l'autenticacio. El token s'ha d'incloure a la capcalera `Authorization`:

```
Authorization: Bearer <token>
```

Alternativament, el token es pot emmagatzemar en una cookie HTTP-only.

---

## Endpoints

### Health Check

#### GET /

Verifica l'estat del servidor.

**Autenticacio:** No requerida

**Resposta:**
```json
{
  "status": "ok",
  "message": "QuietSignal API is running"
}
```

---

### Autenticacio (/auth)

#### POST /auth/register

Registra un nou usuari.

**Autenticacio:** No requerida

**Request Body:**
```json
{
  "name": "string",
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "name": "string",
  "username": "string",
  "email": "string"
}
```

**Errors:**
| Codi | Descripcio |
|------|------------|
| 400 | Username o email ja existeix |
| 422 | Dades invalides |

---

#### POST /auth/login

Autentica un usuari i retorna un token JWT.

**Autenticacio:** No requerida

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Resposta (200):**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Errors:**
| Codi | Descripcio |
|------|------------|
| 401 | Credencials incorrectes |

---

#### POST /auth/logout

Tanca la sessio de l'usuari.

**Autenticacio:** Requerida

**Resposta (200):**
```json
{
  "message": "Successfully logged out"
}
```

---

#### GET /auth/me

Retorna la informacio de l'usuari autenticat.

**Autenticacio:** Requerida

**Resposta (200):**
```json
{
  "id": 1,
  "name": "string",
  "username": "string",
  "email": "string",
  "role": "user"
}
```

---

### Usuaris (/users)

#### POST /users/

Crea un nou usuari (estil administrador).

**Autenticacio:** Requerida (Admin)

**Request Body:**
```json
{
  "name": "string",
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "name": "string",
  "username": "string",
  "email": "string"
}
```

---

#### GET /users/me

Retorna el perfil de l'usuari autenticat.

**Autenticacio:** Requerida

**Resposta (200):**
```json
{
  "id": 1,
  "name": "string",
  "username": "string",
  "email": "string",
  "role": "user"
}
```

---

### Analisi de Sentiments (/analyze)

#### POST /analyze/

Analitza el sentiment d'un text.

**Autenticacio:** Requerida

**Request Body:**
```json
{
  "text": "string"
}
```

**Resposta (200):**
```json
{
  "label": "positive",
  "probabilities": {
    "negative": 0.1,
    "neutral": 0.2,
    "positive": 0.7
  }
}
```

**Valors possibles per a `label`:**
- `negative`
- `neutral`
- `positive`

**Errors:**
| Codi | Descripcio |
|------|------------|
| 400 | Text buit |
| 500 | Error del model ML |

---

### Diaris (/journals)

#### GET /journals/

Llista els diaris de l'usuari autenticat.

**Autenticacio:** Requerida

**Resposta (200):**
```json
[
  {
    "id": 1,
    "title": "string",
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

---

#### POST /journals/?title=X

Crea un nou diari.

**Autenticacio:** Requerida

**Query Parameters:**
| Parametre | Tipus | Descripcio |
|-----------|-------|------------|
| title | string | Titol del diari |

**Resposta (201):**
```json
{
  "id": 1,
  "title": "string",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

#### POST /journals/{journal_id}/entries

Crea una nova entrada al diari.

**Autenticacio:** Requerida

**Path Parameters:**
| Parametre | Tipus | Descripcio |
|-----------|-------|------------|
| journal_id | int | ID del diari |

**Request Body:**
```json
{
  "content": "string"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "content": "string",
  "predictedLabel": "positive",
  "sentimentScore": 0.85,
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

#### GET /journals/{journal_id}/entries

Llista les entrades d'un diari.

**Autenticacio:** Requerida

**Path Parameters:**
| Parametre | Tipus | Descripcio |
|-----------|-------|------------|
| journal_id | int | ID del diari |

**Resposta (200):**
```json
[
  {
    "id": 1,
    "content": "string",
    "predictedLabel": "positive",
    "sentimentScore": 0.85,
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

---

#### GET /journals/{journal_id}/entries/{entry_id}

Obte els detalls d'una entrada.

**Autenticacio:** Requerida

**Path Parameters:**
| Parametre | Tipus | Descripcio |
|-----------|-------|------------|
| journal_id | int | ID del diari |
| entry_id | int | ID de l'entrada |

**Resposta (200):**
```json
{
  "id": 1,
  "content": "string",
  "predictedLabel": "positive",
  "sentimentScore": 0.85,
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

#### POST /journals/{journal_id}/entries/{entry_id}/append

Afegeix un paragraf a una entrada.

**Autenticacio:** Requerida

**Request Body:**
```json
{
  "paragraph": "string"
}
```

---

#### POST /journals/{journal_id}/entries/{entry_id}/append-batch

Afegeix multiples paragrafs a una entrada.

**Autenticacio:** Requerida

**Request Body:**
```json
{
  "paragraphs": ["string", "string"]
}
```

---

### Administracio (/admin)

#### POST /admin/recalculate_entries

Recalcula les prediccions emocionals de totes les entrades.

**Autenticacio:** Requerida (rol: admin)

**Resposta (200):**
```json
{
  "message": "Recalculation completed",
  "entries_processed": 150
}
```

**Errors:**
| Codi | Descripcio |
|------|------------|
| 403 | No autoritzat (requereix rol admin) |

---

## Codis d'Error

| Codi | Significat |
|------|------------|
| 200 | Exit |
| 201 | Creat |
| 400 | Peticio incorrecta |
| 401 | No autenticat |
| 403 | No autoritzat |
| 404 | No trobat |
| 422 | Entitat no processable |
| 500 | Error intern del servidor |

## Exemples d'Us

### Flux Complet d'Autenticacio

```bash
# 1. Registrar usuari
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","username":"test","email":"test@test.com","password":"123456"}'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 3. Utilitzar el token
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <token>"
```

### Analitzar Sentiment

```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"text":"Avui ha estat un dia meravellos!"}'
```

## Rate Limiting

Actualment no hi ha limits de peticions implementats. Es recomana implementar-los en entorns de produccio.

## Versionat

L'API no utilitza versionat a la URL. Futures versions poden incloure el prefix `/api/v1/`.
