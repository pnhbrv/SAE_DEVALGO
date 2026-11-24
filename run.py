# Point d'entrée de l'application (TP 4 et 5)
from monApp import create_app
app = create_app("config.ProductionConfig")
if __name__ == "__main__":
    app.run(debug=True)
