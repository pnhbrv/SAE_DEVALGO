# Point d'entrée de l'application [Source : TP 4 — run.py ; TP 5 — ProductionConfig]
from monApp import create_app
app = create_app("config.ProductionConfig")
if __name__ == "__main__":
    app.run(debug=True)
