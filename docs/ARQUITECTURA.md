# Arquitectura del Sistema

Aquest document descriu l'arquitectura de Apol·lo, incloent els diagrames de classes, casos d'us i l'estructura logica del sistema.

## Visio General

Apol·lo segueix una arquitectura de tres capes:

```
Capa de Presentacio (Frontend)
            |
            v
Capa de Negoci (Backend API)
            |
            v
Capa de Dades (MySQL + ML Model)
```

## Diagrama de Classes - Backend

### Classes Principals

#### User
Representa un usuari del sistema.

```
+------------------------------------------+
|                  User                    |
+------------------------------------------+
| + userId: int                            |
| + username: str                          |
| + password: str                          |
| + diary: Diary                           |
+------------------------------------------+
| + getEntries(start_date, end_date)       |
|   -> list[DiaryEntry]                    |
| + getWeeklySummary(week_start: date)     |
|   -> MoodSummary                         |
+------------------------------------------+
```

#### MoodAnalyzer
Servei d'analisi de sentiments.

```
+------------------------------------------+
|              MoodAnalyzer                |
+------------------------------------------+
| + model: SentimentModel                  |
+------------------------------------------+
| + analyzeEntry(entry: DiaryEntry) -> None|
| + predict(text: str) -> tuple[str, float]|
+------------------------------------------+
```

#### SentimentModel
Encapsula el model de machine learning.

```
+------------------------------------------+
|             SentimentModel               |
+------------------------------------------+
| + modelPath: str                         |
| + loadedModel: Any | None                |
| + labelMapping: dict[int, str]           |
+------------------------------------------+
| + load() -> None                         |
| + preprocess(text: str) -> Any           |
| + predictProba(input: Any) -> list[float]|
| + predictLabel(probs: list) -> str       |
| + predict(text: str) -> tuple[str, float]|
+------------------------------------------+
```

## Diagrama de Casos d'Us

### Actors
- **User**: Usuari registrat del sistema

### Casos d'Us Principals

```
+--------------------------------------------------+
|          Diary Mood Checker Application          |
+--------------------------------------------------+
|                                                  |
|    +----------------+                            |
|    |   Send Text    |                            |
|    +----------------+                            |
|           ^                                      |
|           |                                      |
|     (User)O                                      |
|           |                                      |
|           v                                      |
|    +----------------+                            |
|    | Analyze Mood   |                            |
|    +----------------+                            |
|                                                  |
+--------------------------------------------------+
```

### Descripcio dels Casos d'Us

| Cas d'Us | Descripcio |
|----------|------------|
| Send Text | L'usuari envia text per ser analitzat |
| Analyze Mood | El sistema processa el text i retorna el sentiment |

## Arquitectura de Capes

### Capa de Presentacio (Frontend)

```
src/
    api/
        auth.js          Client d'autenticacio
        analyze.js       Client d'analisi
    components/
        Login.jsx        Formulari de login
        Register.jsx     Formulari de registre
        Analyzer.jsx     Component d'analisi
        Logout.jsx       Boto de logout
    pages/
        AuthPage.jsx     Pagina d'autenticacio
        RegisterPage.jsx Pagina de registre
        AnalyzerPage.jsx Pagina principal
```

### Capa de Negoci (Backend)

```
src/apollo_backend/
    api/
        authRoutes.py    Endpoints d'autenticacio
        analyzeRoutes.py Endpoints d'analisi
        userRoutes.py    Endpoints d'usuaris
    services/
        authService.py   Logica d'autenticacio
        analyzeService.py Logica d'analisi
        userService.py   Logica d'usuaris
    models/
        dto/             Data Transfer Objects
        dao/             Data Access Objects
        entities/        Entitats ORM
```

### Capa de Dades

```
database/
    engine.py        Configuracio de connexio
    session.py       Gestio de sessions
    dbInitializer.py Inicialitzacio de taules

ml/
    modelLoader.py   Carrega del model ML
    preprocess.py    Preprocessament de text
```

## Flux de Dades

### Autenticacio

```
1. Client envia credencials
         |
         v
2. AuthRoutes rep la peticio
         |
         v
3. AuthService valida credencials
         |
         v
4. UserDAO consulta la base de dades
         |
         v
5. JWT generat i retornat al client
```

### Analisi de Sentiments

```
1. Client envia text
         |
         v
2. AnalyzeRoutes rep la peticio
         |
         v
3. AnalyzeService processa
         |
         v
4. ModelLoader executa prediccio
         |
         v
5. Resultat retornat al client
```

## Patrons de Disseny Utilitzats

| Patro | Aplicacio |
|-------|-----------|
| Repository (DAO) | Abstraccio de l'acces a dades |
| Service Layer | Encapsulament de la logica de negoci |
| DTO | Transferencia de dades entre capes |
| Dependency Injection | Injeccio de sessions de BD |
| Factory | Creacio de tokens JWT |

## Seguretat

### Autenticacio
- Tokens JWT amb expiracio configurable
- Algoritme HS256 per signatura
- Contrasenyes encriptades amb bcrypt

### Autoritzacio
- Control d'acces basat en rols (RBAC)
- Rols disponibles: user, admin
- Middleware de validacio en endpoints protegits
