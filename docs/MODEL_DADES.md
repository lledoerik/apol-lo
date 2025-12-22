# Model de Dades

Aquest document descriu l'esquema de la base de dades de Apol·lo, incloent les taules, relacions i restriccions.

## Visio General

Apol·lo utilitza MySQL com a sistema de gestio de bases de dades relacional. L'esquema esta dissenyat per suportar usuaris, diaris, entrades i resums emocionals.

## Diagrama Entitat-Relacio

```
+------------------+       +------------------+
|      users       |       |  mood_summaries  |
+------------------+       +------------------+
| PK userId    INT |<---+  | PK summaryId INT |
|    name  VARCHAR |    |  | FK userId    INT |----+
|    username      |    |  |    weekStart DATE|    |
|    password      |    |  |    weekEnd   DATE|    |
|    email VARCHAR |    |  |    avgMoodScore  |    |
|    createdAt     |    |  |    countNegative |    |
+------------------+    |  |    countNeutral  |    |
         |              |  |    countPositive |    |
         | 1            |  |    totalEntries  |    |
         |              |  |    computedAt    |    |
         v N            |  +------------------+    |
+------------------+    |                          |
|     diaries      |    +--------------------------+
+------------------+
| PK diaryId   INT |
| FK userId    INT |
|    createdAt     |
+------------------+
         |
         | 1
         |
         v N
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

## Taules

### users

Emmagatzema la informacio dels usuaris registrats.

| Columna | Tipus | Restriccions | Descripcio |
|---------|-------|--------------|------------|
| userId | INT | PK, AUTO_INCREMENT | Identificador unic |
| name | VARCHAR(45) | NOT NULL | Nom complet |
| username | VARCHAR(45) | NOT NULL, UNIQUE | Nom d'usuari |
| password | VARCHAR(45) | NOT NULL | Contrasenya encriptada |
| email | VARCHAR(45) | UNIQUE | Correu electronic |
| createdAt | VARCHAR(45) | | Data de creacio |

#### Index
- PRIMARY KEY (userId)
- UNIQUE INDEX (username)
- UNIQUE INDEX (email)

---

### diaries

Emmagatzema els diaris dels usuaris.

| Columna | Tipus | Restriccions | Descripcio |
|---------|-------|--------------|------------|
| diaryId | INT | PK, AUTO_INCREMENT | Identificador unic |
| userId | INT | FK, NOT NULL | Referencia a users |
| createdAt | VARCHAR(45) | | Data de creacio |

#### Relacions
- FK userId REFERENCES users(userId)

#### Index
- PRIMARY KEY (diaryId)
- INDEX (userId)

---

### diaries_entries

Emmagatzema les entrades individuals dels diaris.

| Columna | Tipus | Restriccions | Descripcio |
|---------|-------|--------------|------------|
| entryId | INT | PK, AUTO_INCREMENT | Identificador unic |
| diaryId | INT | FK, NOT NULL | Referencia a diaries |
| createdAt | VARCHAR(45) | | Data de creacio |
| content | TEXT | | Contingut de l'entrada |
| predictedLabel | VARCHAR(45) | | Etiqueta de sentiment |
| sentimentScore | DOUBLE | | Puntuacio de confianca |
| analyzed | TINYINT | DEFAULT 0 | Indica si ha estat analitzat |

#### Relacions
- FK diaryId REFERENCES diaries(diaryId)

#### Index
- PRIMARY KEY (entryId)
- INDEX (diaryId)

---

### mood_summaries

Emmagatzema els resums setmanals d'estat d'anim.

| Columna | Tipus | Restriccions | Descripcio |
|---------|-------|--------------|------------|
| summaryId | INT | PK, AUTO_INCREMENT | Identificador unic |
| userId | INT | FK, NOT NULL | Referencia a users |
| weekStart | DATE | | Inici de la setmana |
| weekEnd | DATE | | Fi de la setmana |
| averageMoodScore | DOUBLE | | Mitjana de puntuacio |
| countNegative | INT | DEFAULT 0 | Entrades negatives |
| countNeutral | INT | DEFAULT 0 | Entrades neutrals |
| countPositive | INT | DEFAULT 0 | Entrades positives |
| totalEntries | INT | DEFAULT 0 | Total d'entrades |
| computedAt | VARCHAR(45) | | Data de calcul |

#### Relacions
- FK userId REFERENCES users(userId)

#### Index
- PRIMARY KEY (summaryId)
- INDEX (userId)
- INDEX (weekStart, weekEnd)

---

## Model Logic

### Taula users (Normalitzada)

```
+--------------------------------------------------+
|                      Users                       |
+--------------------------------------------------+
| PK | int userId                                  |
|    | varchar name                                |
|    | varchar email UNIQUE                        |
|    | timestamptz createdAt                       |
+--------------------------------------------------+
```

## Relacions

| Relacio | Tipus | Descripcio |
|---------|-------|------------|
| users -> diaries | 1:N | Un usuari pot tenir multiples diaris |
| diaries -> diaries_entries | 1:N | Un diari pot tenir multiples entrades |
| users -> mood_summaries | 1:N | Un usuari pot tenir multiples resums |

## Cardinalitat

```
users (1) -------- (N) diaries
                        |
                        | (1)
                        |
                        v (N)
                   diaries_entries

users (1) -------- (N) mood_summaries
```

## Consideracions de Disseny

### Normalitzacio
- L'esquema segueix la Tercera Forma Normal (3NF)
- No hi ha redundancia de dades
- Les dependencies funcionals estan correctament separades

### Integritat Referencial
- Totes les claus foranies tenen restriccions definides
- Els esborrats en cascada no estan habilitats per defecte

### Indexacio
- Index en claus primaries (automatic)
- Index en claus foranies per optimitzar JOINs
- Index en camps de cerca frequents

### Escalabilitat
- Disseny preparat per particionar per userId si es necessari
- Els resums setmanals eviten calculs repetitius

## Scripts SQL

### Creacio de la Base de Dades

```sql
CREATE DATABASE IF NOT EXISTS apollo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### Creacio de Taules

```sql
CREATE TABLE users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    username VARCHAR(45) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(45) UNIQUE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diaries (
    diaryId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(userId)
);

CREATE TABLE diaries_entries (
    entryId INT AUTO_INCREMENT PRIMARY KEY,
    diaryId INT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content TEXT,
    predictedLabel VARCHAR(45),
    sentimentScore DOUBLE,
    analyzed TINYINT DEFAULT 0,
    FOREIGN KEY (diaryId) REFERENCES diaries(diaryId)
);

CREATE TABLE mood_summaries (
    summaryId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    weekStart DATE,
    weekEnd DATE,
    averageMoodScore DOUBLE,
    countNegative INT DEFAULT 0,
    countNeutral INT DEFAULT 0,
    countPositive INT DEFAULT 0,
    totalEntries INT DEFAULT 0,
    computedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(userId)
);
```
