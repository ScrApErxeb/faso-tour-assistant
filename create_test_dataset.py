import json
from datetime import datetime

print("=" * 60)
print("📝 CRÉATION DU DATASET DE TEST")
print("=" * 60)

# Dataset de 20 questions-réponses sur le tourisme burkinabè
test_dataset = [
    {
        "id": "q001",
        "question": "Qu'est-ce que le FESPACO ?",
        "reponse": "Le FESPACO (Festival Panafricain du Cinéma et de la Télévision de Ouagadougou) est le plus grand festival de cinéma d'Afrique. Il est organisé tous les deux ans à Ouagadougou depuis 1969 et attire des cinéastes de tout le continent africain et du monde entier.",
        "categorie": "culture",
        "difficulte": "facile"
    },
    {
        "id": "q002",
        "question": "Où se trouvent les Pics de Sindou ?",
        "reponse": "Les Pics de Sindou se trouvent dans le sud-ouest du Burkina Faso. Ce sont des formations géologiques spectaculaires en grès sculptées par l'érosion.",
        "categorie": "sites_naturels",
        "difficulte": "facile"
    },
    {
        "id": "q003",
        "question": "Qu'est-ce que le SIAO ?",
        "reponse": "Le SIAO (Salon International de l'Artisanat de Ouagadougou) est une vitrine de l'artisanat africain qui se tient à Ouagadougou tous les deux ans. Il rassemble des artisans de toute l'Afrique présentant bronze, tissage, cuir et sculptures.",
        "categorie": "culture",
        "difficulte": "facile"
    },
    {
        "id": "q004",
        "question": "Quel est le premier site du Burkina Faso inscrit au patrimoine mondial de l'UNESCO ?",
        "reponse": "Les Ruines de Loropéni sont le premier site du Burkina Faso inscrit au patrimoine mondial de l'UNESCO en 2009. Ces ruines fortifiées témoignent du commerce transsaharien de l'or.",
        "categorie": "patrimoine",
        "difficulte": "moyen"
    },
    {
        "id": "q005",
        "question": "Où se trouvent les Cascades de Karfiguéla ?",
        "reponse": "Les Cascades de Karfiguéla sont situées près de Banfora dans le sud-ouest du Burkina Faso. Elles sont une attraction touristique majeure pendant la saison des pluies avec leurs chutes d'eau impressionnantes.",
        "categorie": "sites_naturels",
        "difficulte": "facile"
    },
    {
        "id": "q006",
        "question": "Quelle est la fréquence d'organisation du FESPACO ?",
        "reponse": "Le FESPACO est organisé tous les deux ans (biennale) à Ouagadougou.",
        "categorie": "culture",
        "difficulte": "facile"
    },
    {
        "id": "q007",
        "question": "Citez trois types d'artisanat présentés au SIAO",
        "reponse": "Au SIAO, on trouve notamment le bronze, le tissage et le travail du cuir. D'autres formes incluent les sculptures, la poterie et la maroquinerie.",
        "categorie": "artisanat",
        "difficulte": "moyen"
    },
    {
        "id": "q008",
        "question": "Depuis quelle année le FESPACO existe-t-il ?",
        "reponse": "Le FESPACO existe depuis 1969.",
        "categorie": "culture",
        "difficulte": "moyen"
    },
    {
        "id": "q009",
        "question": "Quelle est la particularité géologique des Pics de Sindou ?",
        "reponse": "Les Pics de Sindou sont des formations en grès sculptées par l'érosion au fil du temps, créant des pics et des formations rocheuses spectaculaires.",
        "categorie": "sites_naturels",
        "difficulte": "moyen"
    },
    {
        "id": "q010",
        "question": "Dans quelle ville se déroule le FESPACO ?",
        "reponse": "Le FESPACO se déroule à Ouagadougou, la capitale du Burkina Faso.",
        "categorie": "culture",
        "difficulte": "facile"
    },
    {
        "id": "q011",
        "question": "Quelle est l'importance historique des Ruines de Loropéni ?",
        "reponse": "Les Ruines de Loropéni témoignent du commerce transsaharien de l'or. Ces fortifications anciennes représentent un patrimoine historique important lié aux routes commerciales de l'Afrique de l'Ouest.",
        "categorie": "patrimoine",
        "difficulte": "difficile"
    },
    {
        "id": "q012",
        "question": "Quelle est la meilleure période pour visiter les Cascades de Karfiguéla ?",
        "reponse": "La meilleure période pour visiter les Cascades de Karfiguéla est pendant la saison des pluies, quand les chutes d'eau sont les plus impressionnantes.",
        "categorie": "sites_naturels",
        "difficulte": "moyen"
    },
    {
        "id": "q013",
        "question": "Le SIAO rassemble des artisans de quelle zone géographique ?",
        "reponse": "Le SIAO rassemble des artisans de toute l'Afrique, faisant de ce salon une vitrine continentale de l'artisanat africain.",
        "categorie": "artisanat",
        "difficulte": "facile"
    },
    {
        "id": "q014",
        "question": "Quel type de festival est le FESPACO ?",
        "reponse": "Le FESPACO est un festival de cinéma et de télévision. C'est le plus grand festival cinématographique d'Afrique, dédié au cinéma africain et de la diaspora.",
        "categorie": "culture",
        "difficulte": "facile"
    },
    {
        "id": "q015",
        "question": "En quelle année les Ruines de Loropéni ont-elles été inscrites au patrimoine UNESCO ?",
        "reponse": "Les Ruines de Loropéni ont été inscrites au patrimoine mondial de l'UNESCO en 2009.",
        "categorie": "patrimoine",
        "difficulte": "moyen"
    },
    {
        "id": "q016",
        "question": "Quels sont les principaux sites touristiques naturels du Burkina Faso ?",
        "reponse": "Les principaux sites naturels incluent les Pics de Sindou (formations rocheuses), les Cascades de Karfiguéla près de Banfora, et la Réserve de Nazinga pour observer les éléphants.",
        "categorie": "sites_naturels",
        "difficulte": "moyen"
    },
    {
        "id": "q017",
        "question": "Quelle est la dimension panafricaine du FESPACO ?",
        "reponse": "Le FESPACO est panafricain car il attire des cinéastes de tout le continent africain et met en valeur le cinéma africain dans sa diversité. C'est un lieu de rencontre et d'échange pour les professionnels du cinéma de toute l'Afrique.",
        "categorie": "culture",
        "difficulte": "difficile"
    },
    {
        "id": "q018",
        "question": "Où se situe géographiquement Banfora au Burkina Faso ?",
        "reponse": "Banfora se situe dans le sud-ouest du Burkina Faso. C'est une ville proche de plusieurs sites touristiques majeurs comme les Cascades de Karfiguéla et les Pics de Sindou.",
        "categorie": "geographie",
        "difficulte": "moyen"
    },
    {
        "id": "q019",
        "question": "Quels types d'objets artisanaux peut-on trouver au SIAO ?",
        "reponse": "Au SIAO, on trouve divers objets artisanaux : sculptures en bronze, tissus traditionnels, articles en cuir (maroquinerie), poteries, masques, bijoux et autres créations artisanales africaines.",
        "categorie": "artisanat",
        "difficulte": "facile"
    },
    {
        "id": "q020",
        "question": "Pourquoi le FESPACO est-il important pour l'Afrique ?",
        "reponse": "Le FESPACO est important car c'est le plus grand festival de cinéma d'Afrique. Il valorise le cinéma africain, offre une plateforme aux cinéastes du continent, favorise les échanges culturels et contribue au rayonnement culturel du Burkina Faso et de l'Afrique.",
        "categorie": "culture",
        "difficulte": "difficile"
    }
]

# Statistiques du dataset
print("\n[INFO] 📊 Création du dataset...")
print(f"[INFO]   • {len(test_dataset)} questions-réponses")

categories = {}
difficultes = {}

for item in test_dataset:
    cat = item['categorie']
    diff = item['difficulte']
    categories[cat] = categories.get(cat, 0) + 1
    difficultes[diff] = difficultes.get(diff, 0) + 1

print(f"\n[INFO] 📋 RÉPARTITION PAR CATÉGORIE:")
for cat, count in sorted(categories.items()):
    print(f"[INFO]   • {cat}: {count} questions")

print(f"\n[INFO] 🎯 RÉPARTITION PAR DIFFICULTÉ:")
for diff, count in sorted(difficultes.items()):
    print(f"[INFO]   • {diff}: {count} questions")

# Sauvegarder le dataset
output_file = 'evaluation/test_dataset.json'

try:
    # Créer le fichier avec métadonnées
    final_dataset = {
        "metadata": {
            "nom": "Dataset Test - Tourisme Burkina Faso",
            "description": "20 questions-réponses pour évaluer le système RAG",
            "date_creation": datetime.now().isoformat(),
            "nombre_questions": len(test_dataset),
            "categories": list(categories.keys()),
            "difficultes": list(difficultes.keys())
        },
        "questions": test_dataset
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n[SAVE] ✓ Dataset sauvegardé: {output_file}")
    
except Exception as e:
    print(f"\n[SAVE] ✗ Erreur: {e}")

print("\n" + "=" * 60)
print("✅ DATASET DE TEST CRÉÉ")
print("=" * 60)
print(f"\n📁 FICHIER CRÉÉ:")
print(f"   ✓ {output_file}")
print("\n💡 Le dataset contient 20 questions avec leurs réponses")
print("   de référence pour évaluer la qualité du RAG.")
print("=" * 60)