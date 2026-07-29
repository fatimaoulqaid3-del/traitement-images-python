# 🏥 Cabinet Médical — Application Full Stack

Plateforme de gestion médicale complète avec React.js, Node.js/Express, et MongoDB.

---

## 🏗️ Architecture

```
cabinet-medical/
├── xml/                    # Phase 1 — Modèle de données XML + XSD
│   ├── patients.xml
│   └── patients.xsd
├── backend/                # Phase 3 — API REST Node.js/Express
│   ├── models/             # Schémas Mongoose
│   ├── routes/             # Endpoints REST
│   ├── middleware/         # Auth JWT
│   ├── scripts/seed.js     # Phase 2 — Seed XML → MongoDB
│   └── server.js
├── frontend/               # Phase 4 — React.js
│   └── src/
│       ├── components/     # UI Components
│       ├── context/        # AuthContext
│       ├── pages/          # Layouts
│       └── services/       # API axios
└── docker-compose.yml      # Phase 5 — Déploiement Docker
```

---

## 🐳 Démarrage rapide (Docker)

### 1. Prérequis
- Docker Desktop installé et en cours d'exécution

### 2. Lancer tous les services
```bash
docker compose up --build
```

### 3. Importer les données de démo (XML → MongoDB)
Dans un autre terminal, une fois les conteneurs démarrés :
```bash
docker exec -it cabinet_backend node scripts/seed.js
```

### 4. Accéder à l'application
| Service   | URL                        |
|-----------|----------------------------|
| Frontend  | http://localhost:3000      |
| API REST  | http://localhost:5000/api  |
| MongoDB   | mongodb://localhost:27017  |

---

## 🔑 Comptes de démo

| Rôle     | Email                       | Mot de passe |
|----------|-----------------------------|--------------|
| Médecin  | dr.martin@cabinet.fr        | medecin123   |
| Patient  | sophie.bernard@email.fr     | patient123   |
| Patient  | marc.lefebvre@email.fr      | patient123   |

---

## 🧑‍💻 Développement local (sans Docker)

### Backend
```bash
cd backend
npm install
# Modifier .env : MONGO_URI=mongodb://localhost:27017/cabinet_medical
npm run seed      # Importer les données
npm run dev       # Démarrer le serveur (nodemon)
```

### Frontend
```bash
cd frontend
npm install
# Créer .env.local :
# REACT_APP_API_URL=http://localhost:5000/api
npm start
```

---

## 🗄️ Collections MongoDB

| Collection      | Description                              |
|-----------------|------------------------------------------|
| `patients`      | Dossiers patients complets (12 de base)  |
| `consultations` | Historique des consultations (~60)       |
| `rendezvous`    | Rendez-vous passés & futurs (~40)        |
| `ordonnances`   | Ordonnances avec médicaments (~30)       |
| `examens`       | Résultats d'examens (~40)                |
| `users`         | Comptes médecin & patient                |

---

## 🔌 Endpoints API

### Auth
```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Patients
```
GET    /api/patients
GET    /api/patients/:id
POST   /api/patients         (médecin only)
PUT    /api/patients/:id     (médecin only)
DELETE /api/patients/:id     (médecin only)
```

### Consultations / RDV / Ordonnances / Examens
```
GET  /api/consultations?patientId=P-00001
POST /api/consultations

GET  /api/rendez-vous?date=2026-04-26
POST /api/rendez-vous
PUT  /api/rendez-vous/:id
DELETE /api/rendez-vous/:id

GET  /api/ordonnances
POST /api/ordonnances

GET  /api/examens
POST /api/examens
PUT  /api/examens/:id

GET  /api/stats/dashboard
```

---

## 🖥️ Fonctionnalités

### Espace Médecin
- 📊 **Dashboard** — Métriques en temps réel, RDV du jour, répartition patients
- 👥 **Patients** — Grille, recherche, filtres par statut, dossier complet, CRUD
- 📅 **Agenda** — Calendrier mensuel, liste des RDV, gestion complète
- 🩺 **Consultations** — Enregistrement avec constantes vitales, historique
- 💊 **Ordonnances** — Multi-médicaments, renouvellement
- 🔬 **Examens** — Prescription, résultats, mise à jour statut
- 📈 **Statistiques** — Graphiques Recharts (barres + camembert)

### Espace Patient
- 🏠 **Accueil** — Résumé personnalisé, constantes, prochains RDV
- 📅 **Mes RDV** — Upcoming + historique
- 📋 **Mon dossier** — Infos médicales complètes, historique consultations
- 🔬 **Mes résultats** — Examens avec valeurs biologiques
- 💊 **Mes ordonnances** — Liste détaillée des prescriptions

---

## 📦 Technologies

| Couche    | Stack                                    |
|-----------|------------------------------------------|
| Frontend  | React 18, React Router 6, Axios, Recharts|
| Backend   | Node.js 20, Express 4, JWT, bcryptjs     |
| Base de données | MongoDB 7, Mongoose 8              |
| DevOps    | Docker, Docker Compose, Nginx            |
| Données   | XML + XSD (validation schéma)            |
