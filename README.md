# 📊 Dashboard : Analyse des ventes d’un supermarché

Ce projet est une application **[Dash](https://dash.plotly.com/)** permettant d’analyser les ventes d’un supermarché à partir du dataset `supermarket_sales.csv`.  
L’application est déployée en ligne grâce à **Render**.

 **Démo en ligne : [projet-python.onrender.com](https://projet-python.onrender.com/)**

---

##  Fonctionnalités
- Filtres interactifs par **sexe** et **ville**
- Indicateurs clés :
  - **Total des achats**
  - **Nombre d’achats**
- Graphiques dynamiques :
  - Histogramme de la répartition des montants
  - Nombre total d’achats par sexe et par ville
  - Répartition des produits (camembert)
- Design responsive avec un thème en dégradé bleu

---

##  Structure du projet
- `app.py` → code principal de l’application Dash  
- `supermarket_sales.csv` → dataset utilisé  
- `requirements.txt` → dépendances Python  
- `Procfile` → configuration du déploiement sur Render  

---

##  Installation locale
Clone le projet et installe les dépendances :

```bash
git clone https://github.com/estellemtz/projet_python.git
cd projet_python
pip install -r requirements.txt
python app.py
