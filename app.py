from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)

categories = {
    "animaux": ["chat", "chien", "lion", "elephant", "tigre", "girafe", "zebre", "ours", "singe", "crocodile", "hippopotame", "rhinoceros", "kangourou", "souris", "cheval", "ecureuil", "chameau", "pingouin", "panda", "koala", "alligator", "autruche", "herisson", "furet", "renard", "hibou", "loutre", "castor", "perroquet", "poulet", "bison", "dromadaire", "lezard", "serpent", "poule", "coq", "canard", "cygne", "colibri", "abeille", "fourmi", "papillon", "coccinelle", "moustique", "guepe", "scarabee", "chauve-souris", "pelican"],
    "fruits": ["pomme", "banane", "orange", "fraise", "kiwi", "cerise", "pasteque", "raisin", "ananas", "poire", "abricot", "peche", "mangue", "framboise", "cassis"],
    "pays": ["france", "espagne", "italie", "canada", "japon", "australie", "allemagne", "bresil", "russie", "mexique", "chine", "inde", "afrique du sud", "argentine", "egypte"],
    "legumes": ["carotte", "brocoli", "pomme de terre", "tomate", "concombre", "chou", "poivron", "courgette", "aubergine", "oignon", "ail", "celeri", "radis", "epinard"],
    "sports": ["football", "tennis", "natation", "basketball", "volleyball", "baseball", "golf", "rugby", "cyclisme", "athletisme", "boxe", "escrime", "halterophilie", "plongeon"],
    "marques": ["apple", "google", "amazon", "microsoft", "samsung", "facebook", "tesla", "coca-cola", "pepsi", "nike", "adidas", "mcdonald's", "burger king", "sony"],
    "acteurs_americains": ["tom hanks", "leonardo dicaprio", "brad pitt", "johnny depp", "robert downey jr.", "morgan freeman", "denzel washington", "kevin spacey", "harrison ford", "samuel l. jackson"],
    "acteurs_francais": ["jean reno", "gerard depardieu", "omar sy", "vincent cassel", "jean dujardin", "daniel auteuil", "jean-paul belmondo", "alain delon", "louis de funes", "jacques tati"],
    "metiers": ["medecin", "enseignant", "ingenieur", "avocat", "informaticien", "architecte", "infirmier", "plombier","electricien", "boulanger", "patissier", "chef cuisinier", "coiffeur", "jardinier", "chauffeur de taxi","mecanicien", "artiste", "acteur", "musicien", "ecrivain", "journaliste", "serveur", "pompier", "policier","militaire", "agriculteur", "pharmacien", "dentiste", "veterinaire", "facteur", "couturier", "couturiere","tailleur", "banquier", "comptable", "economiste", "chef de projet", "biologiste", "chimiste", "psychologue","psychanalyste", "sociologue", "historien", "geologue", "astronome", "artiste martial", "danseur","eboueur", "plongeur sous-marin", "serrurier"],
    "ecrivains_francais": ["Victor Hugo", "Marcel Proust", "Albert Camus", "Emile Zola", "Gustave Flaubert", "Jean-Paul Sartre","Simone de Beauvoir", "Antoine de Saint-Exupery", "Alexandre Dumas", "Honore de Balzac", "Andre Gide","Marguerite Duras", "Voltaire", "Moliere", "Gustave Eiffel", "Jean-Jacques Rousseau", "Charles Baudelaire","Francois Rabelais", "Anatole France", "Jules Verne", "Andre Malraux", "Jean Cocteau", "Guillaume Apollinaire","Romain Gary", "Paul Valery", "Paul Eluard", "Louis-Ferdinand Celine", "Albert Camus", "Francois Mauriac","Andre Breton", "Jean Anouilh", "Jean Genet", "Sylvia Plath", "Francoise Sagan", "Julien Gracq","Michel Houellebecq", "Patrick Modiano", "Boris Vian", "Pierre Loti", "Pierre Corneille", "Jean Racine","Pierre de Ronsard", "Paul Verlaine", "Arthur Rimbaud", "Stendhal", "Gerard de Nerval", "Gustave Dore","Theophile Gautier", "Andre Maurois", "Alfred de Musset", "Stephane Mallarme"]
}


pseudo = ""
categorie = ""
mot_secret = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global pseudo, categorie, mot_secret
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        categorie = request.form["categorie"]
        mots = categories[categorie]
        mot_secret = random.choice(mots)
        return render_template("loading.html", pseudo=pseudo, categorie=categorie, mot_secret=mot_secret)
    return render_template("index.html")

@app.route("/loading", methods=["GET", "POST"])
def loading():
    global pseudo, categorie, mot_secret
    return render_template("loading.html", pseudo=pseudo, categorie=categorie, mot_secret=mot_secret)

def toutes_lettres_devinées(mot_secret, lettres_devinees):
    for lettre in mot_secret:
        if lettre not in lettres_devinees:
            return False
    return True

@app.route("/pendu", methods=["GET", "POST"])
def jeu_pendu():
    global pseudo, categorie, mot_secret
    if request.method == "POST":
        lettres_devinees = list(request.form.get("lettres_devinees", ""))
        essais_restants = int(request.form.get("essais_restants", 6))

        lettre = request.form["lettre"].lower()

        if lettre in lettres_devinees:
            message = "Vous avez déjà deviné cette lettre."
        else:
            lettres_devinees.append(lettre)

            if lettre in mot_secret:
                message = "Bonne devinette !"
            else:
                message = "Mauvaise devinette."
                essais_restants -= 1

        if toutes_lettres_devinées(mot_secret, lettres_devinees):
            message = "Félicitations ! Vous avez deviné le mot : " + mot_secret
            return render_template("win.html", message=message)

        if essais_restants == 0 and not toutes_lettres_devinées(mot_secret, lettres_devinees):
            message = "Vous avez perdu ! Le mot était : " + mot_secret
            return render_template("defeat.html", message=message)

        return render_template("pendu.html", pseudo=pseudo, categorie=categorie, mot_secret=mot_secret, essais=essais_restants, message=message,
                               lettres_devinees="".join(lettres_devinees))
    return render_template("pendu.html", pseudo=pseudo, categorie=categorie, mot_secret=mot_secret, essais=6, message="", lettres_devinees="")

@app.route("/accueil")
def accueil():
    # Ajoutez cette route pour rediriger vers la page d'accueil après la fin du jeu
    global pseudo, categorie, mot_secret
    pseudo = ""
    categorie = ""
    mot_secret = ""
    return redirect(url_for("index"))

