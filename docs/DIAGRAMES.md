# Diagrames del Sistema

Aquest document conté tots els diagrames tècnics del projecte QuietSignal.

---

## Diagrama de Classes - Backend

### MoodAnalyzer

Servei principal d'anàlisi de sentiments.

```
+--------------------------------------------------+
|                   MoodAnalyzer                   |
+--------------------------------------------------+
| + model: SentimentModel                          |
+--------------------------------------------------+
| + analyzeEntry(entry: DiaryEntry) -> None        |
| + predict(text: str) -> tuple[str, float]        |
+--------------------------------------------------+
                        |
                        | utilitza
                        v
+--------------------------------------------------+
|                  SentimentModel                  |
+--------------------------------------------------+
| + modelPath: str                                 |
| + loadedModel: Any | None                        |
| + labelMapping: dict[int, str]                   |
+--------------------------------------------------+
| + load() -> None                                 |
| + preprocess(text: str) -> Any                   |
| + predictProba(processed_input: Any) -> list     |
| + predictLabel(probabilities: list) -> str       |
| + predict(text: str) -> tuple[str, float]        |
+--------------------------------------------------+
```

### User

Entitat d'usuari del sistema.

```
+--------------------------------------------------+
|                      User                        |
+--------------------------------------------------+
| + userId: int                                    |
| + username: str                                  |
| + password: str                                  |
| + diary: Diary                                   |
+--------------------------------------------------+
| + getEntries(start_date, end_date) -> list       |
| + getWeeklySummary(week_start: date) -> Summary  |
+--------------------------------------------------+
```

---

## Diagrama de Casos d'Ús

```
+----------------------------------------------------------+
|              Diary Mood Checker Application              |
+----------------------------------------------------------+
|                                                          |
|                     +---------------+                    |
|                     |   Send Text   |                    |
|                     +---------------+                    |
|                            ^                             |
|                            |                             |
|                       (User)                             |
|                            |                             |
|                            v                             |
|                     +---------------+                    |
|                     | Analyze Mood  |                    |
|                     +---------------+                    |
|                                                          |
+----------------------------------------------------------+
```

### Descripció dels Casos d'Ús

| Cas d'Ús | Actor | Descripció |
|----------|-------|------------|
| Send Text | User | L'usuari introdueix text per ser analitzat |
| Analyze Mood | System | El sistema processa el text i retorna el sentiment detectat |

---

## Diagrama Entitat-Relació

```
+------------------+          +------------------+
|      users       |          |  mood_summaries  |
+------------------+          +------------------+
| PK userId    INT |<------+  | PK summaryId INT |
|    name  VARCHAR |       |  | FK userId    INT |---+
|    username      |       |  |    weekStart DATE|   |
|    password      |       |  |    weekEnd   DATE|   |
|    email VARCHAR |       |  |    avgMoodScore  |   |
|    createdAt     |       |  |    countNegative |   |
+------------------+       |  |    countNeutral  |   |
         |                 |  |    countPositive |   |
         | 1:N             |  |    totalEntries  |   |
         v                 |  |    computedAt    |   |
+------------------+       |  +------------------+   |
|     diaries      |       |                        |
+------------------+       +------------------------+
| PK diaryId   INT |
| FK userId    INT |
|    createdAt     |
+------------------+
         |
         | 1:N
         v
+------------------+
|  diaries_entries |
+------------------+
| PK entryId   INT |
| FK diaryId   INT |
|    createdAt     |
|    content  TEXT |
|    predictedLabel|
|    sentimentScore|
|    analyzed      |
+------------------+
```

### Relacions

| Taula Origen | Taula Destí | Cardinalitat | Descripció |
|--------------|-------------|--------------|------------|
| users | diaries | 1:N | Un usuari pot tenir múltiples diaris |
| diaries | diaries_entries | 1:N | Un diari pot tenir múltiples entrades |
| users | mood_summaries | 1:N | Un usuari pot tenir múltiples resums setmanals |

---

## Model Lògic de Dades

### Taula Users

```
+--------------------------------------------------+
|                      Users                       |
+--------------------------------------------------+
| PK | int userId                                  |
|    | varchar name                                |
|    | varchar username UNIQUE                     |
|    | varchar password                            |
|    | varchar email UNIQUE                        |
|    | timestamptz createdAt                       |
+--------------------------------------------------+
```

### Taula Diaries

```
+--------------------------------------------------+
|                     Diaries                      |
+--------------------------------------------------+
| PK | int diaryId                                 |
| FK | int userId -> Users(userId)                 |
|    | timestamptz createdAt                       |
+--------------------------------------------------+
```

### Taula Diaries_Entries

```
+--------------------------------------------------+
|                  Diaries_Entries                 |
+--------------------------------------------------+
| PK | int entryId                                 |
| FK | int diaryId -> Diaries(diaryId)             |
|    | timestamptz createdAt                       |
|    | text content                                |
|    | varchar predictedLabel                      |
|    | double sentimentScore                       |
|    | tinyint analyzed                            |
+--------------------------------------------------+
```

### Taula Mood_Summaries

```
+--------------------------------------------------+
|                  Mood_Summaries                  |
+--------------------------------------------------+
| PK | int summaryId                               |
| FK | int userId -> Users(userId)                 |
|    | date weekStart                              |
|    | date weekEnd                                |
|    | double averageMoodScore                     |
|    | int countNegative                           |
|    | int countNeutral                            |
|    | int countPositive                           |
|    | int totalEntries                            |
|    | timestamptz computedAt                      |
+--------------------------------------------------+
```

---

## Wireframes de la Interfície

### Pantalla d'Anàlisi

```
+----------------------------------------------------------+
| +--------+                                    [  Avatar  ]|
| | logout |                                                |
| +--------+                                                |
|                                                           |
|   +---------------------------------------------------+   |
|   |                                                   |   |
|   |                                                   |   |
|   |              Àrea d'entrada de text               |   |
|   |                                                   |   |
|   |                                                   |   |
|   +---------------------------------------------------+   |
|                                                           |
|                    +-------------+                        |
|                    |   analyze   |                        |
|                    +-------------+                        |
|                                                           |
+----------------------------------------------------------+
```

### Pantalla de Login

```
+----------------------------------------------------------+
|                                                           |
|                                                           |
|                 +---------------------+                   |
|                 |     username        |                   |
|                 +---------------------+                   |
|                                                           |
|                 +---------------------+                   |
|                 |     password        |                   |
|                 +---------------------+                   |
|                                                           |
|                 +----------+  +----------+                |
|                 | register |  |  login   |                |
|                 +----------+  +----------+                |
|                                                           |
+----------------------------------------------------------+
```

### Pantalla de Registre

```
+----------------------------------------------------------+
|                                                           |
|                 +---------------------+                   |
|                 |       name          |                   |
|                 +---------------------+                   |
|                                                           |
|                 +---------------------+                   |
|                 |     username        |                   |
|                 +---------------------+                   |
|                                                           |
|                 +---------------------+                   |
|                 |     password        |                   |
|                 +---------------------+                   |
|                                                           |
|                 +---------------------+                   |
|                 |  confirm password   |                   |
|                 +---------------------+                   |
|                                                           |
|                 +---------------------+                   |
|                 |      Register       |                   |
|                 +---------------------+                   |
|                                                           |
+----------------------------------------------------------+
```

---

## Flux de Navegació

```
+----------+     +----------+     +----------+
|  Login   | --> | Analyze  | --> |  Logout  |
+----------+     +----------+     +----------+
     |                                  |
     v                                  |
+----------+                            |
| Register | ---------------------------+
+----------+
```
