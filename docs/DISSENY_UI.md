# Disseny de la Interficie d'Usuari

Aquest document descriu els wireframes i especificacions de la interficie d'usuari de QuietSignal.

## Visio General

L'aplicacio consta de tres pantalles principals:

1. Pantalla de Login
2. Pantalla de Registre
3. Pantalla d'Analisi

## Wireframes

### Pantalla de Login

```
+--------------------------------------------------+
|                                                  |
|                                                  |
|           +------------------------+             |
|           |      username          |             |
|           +------------------------+             |
|                                                  |
|           +------------------------+             |
|           |      password          |             |
|           +------------------------+             |
|                                                  |
|           +-----------+ +-----------+            |
|           | register  | |   login   |            |
|           +-----------+ +-----------+            |
|                                                  |
|                                                  |
+--------------------------------------------------+
```

#### Especificacions

| Element | Tipus | Descripcio |
|---------|-------|------------|
| username | Input text | Camp per al nom d'usuari |
| password | Input password | Camp per a la contrasenya |
| register | Button | Navega a la pantalla de registre |
| login | Button | Envia les credencials per autenticar |

#### Comportament
- En fer clic a "login", es validen les credencials
- Si son correctes, redirigeix a la pantalla d'analisi
- Si son incorrectes, mostra missatge d'error
- El boto "register" navega a la pantalla de registre

---

### Pantalla de Registre

```
+--------------------------------------------------+
|                                                  |
|                                                  |
|           +------------------------+             |
|           |        name            |             |
|           +------------------------+             |
|                                                  |
|           +------------------------+             |
|           |      username          |             |
|           +------------------------+             |
|                                                  |
|           +------------------------+             |
|           |      password          |             |
|           +------------------------+             |
|                                                  |
|           +------------------------+             |
|           |   confirm password     |             |
|           +------------------------+             |
|                                                  |
|           +------------------------+             |
|           |       Register         |             |
|           +------------------------+             |
|                                                  |
+--------------------------------------------------+
```

#### Especificacions

| Element | Tipus | Descripcio |
|---------|-------|------------|
| name | Input text | Nom complet de l'usuari |
| username | Input text | Nom d'usuari unic |
| password | Input password | Contrasenya (minim 6 caracters) |
| confirm password | Input password | Confirmacio de la contrasenya |
| Register | Button | Envia el formulari de registre |

#### Validacions
- Tots els camps son obligatoris
- El username ha de ser unic
- La contrasenya ha de tenir minim 6 caracters
- Les contrasenyes han de coincidir

---

### Pantalla d'Analisi

```
+--------------------------------------------------+
| +--------+                                       |
| | logout |                          ( avatar )   |
| +--------+                                       |
|                                                  |
|  +--------------------------------------------+  |
|  |                                            |  |
|  |                                            |  |
|  |           Area de text                     |  |
|  |                                            |  |
|  |                                            |  |
|  +--------------------------------------------+  |
|                                                  |
|           +------------------------+             |
|           |       analyze          |             |
|           +------------------------+             |
|                                                  |
|                                                  |
+--------------------------------------------------+
```

#### Especificacions

| Element | Tipus | Descripcio |
|---------|-------|------------|
| logout | Button | Tanca la sessio i redirigeix al login |
| avatar | Image | Imatge de perfil de l'usuari |
| Area de text | Textarea | Camp per introduir el text a analitzar |
| analyze | Button | Envia el text per analitzar el sentiment |

#### Comportament
- L'usuari escriu text a l'area de text
- En fer clic a "analyze", s'envia el text al backend
- Es mostra el resultat de l'analisi (positiu, neutral, negatiu)
- El boto "logout" tanca la sessio

---

## Flux de Navegacio

```
                    +------------------+
                    |                  |
                    v                  |
+--------+     +--------+         +----------+
| Login  | --> | Analisi| ------> |  Logout  |
+--------+     +--------+         +----------+
    |                                   |
    v                                   |
+----------+                            |
| Registre | ---------------------------+
+----------+
```

## Guia d'Estils

### Colors
L'aplicacio utilitza una paleta de colors neutres amb accents per als elements interactius.

### Tipografia
- Font principal: Sistema (sans-serif)
- Mida base: 16px

### Components

#### Botons
- Estil primari per a accions principals (login, analyze)
- Estil secundari per a accions secundaries (register, logout)

#### Inputs
- Borde subtil
- Estat focus amb borde destacat
- Missatges d'error en vermell

#### Layout
- Centrat verticalment i horitzontalment
- Maxima amplada de 400px per als formularis
- Espaiat consistent entre elements

## Responsivitat

L'aplicacio es responsiva i s'adapta a diferents mides de pantalla:

| Dispositiu | Amplada | Adaptacions |
|------------|---------|-------------|
| Mobil | < 640px | Formularis a amplada completa |
| Tablet | 640px - 1024px | Formularis centrats |
| Desktop | > 1024px | Formularis centrats amb maxima amplada |
