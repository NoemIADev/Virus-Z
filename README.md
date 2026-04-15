# 🧟 Virus Z - Projet POC

## 📌 Présentation

Virus Z est un projet de type **Proof of Concept (POC)** réalisé dans le cadre d’une formation.

Le but est de simuler la gestion d’une épidémie avec :
- ajout de cas infectés
- gestion des zones de quarantaine
- visualisation sur une carte
- système d’alertes par email

---

## ⚙️ Stack technique

- **Backend API** : FastAPI  
- **Frontend** : Streamlit  
- **Base de données** : MySQL + SQLite  
- **Carte** : Folium  
- **Mailing** : Azure Communication Services  

Librairies principales : voir `requirements.txt`

---

## 🧱 Architecture

Frontend (Streamlit)  
↓  
API (FastAPI)  
↓  
Base MySQL (cas, virus, adresses)  

+ Service alertes (Flask + SQLite + Email)

---

## 🚀 Fonctionnalités

### ➕ Ajout de cas
Formulaire en 3 étapes :
1. Infos générales
2. Quarantaine ou lieux
3. Validation + envoi API  

---

### 🌍 Carte des cas
- Affichage des cas géolocalisés  
- Couleur différente par virus  

---

### 🔌 API

Routes principales :
- `POST /cases` → créer un cas  
- `GET /cases/map` → données carte  
- `GET /cases/count` → nombre de cas  
- `GET /catalog/...` → listes (virus, zones)  

---

### 📩 Alertes email

- seuil ORANGE / ROUGE selon nb de cas  
- envoi automatique aux abonnés  
- stockage dans SQLite  

---

## 🗄️ Base de données

- **MySQL** → données principales  
- **SQLite** → alertes et abonnés  

---

## ▶️ Lancer le projet

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
