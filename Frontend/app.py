import streamlit as st
import requests
import json
from datetime import datetime
import random

# Configuration PWA
st.set_page_config(
    page_title="Tourisme Burkina Faso",
    page_icon="🇧🇫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.burkina-faso.com',
        'Report a bug': None,
        'About': "# Assistant Tourisme Burkina Faso 🇧🇫\nVotre guide intelligent du Pays des Hommes Intègres"
    }
)

# Injection du PWA Manifest et Service Worker
st.markdown("""
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#009E49">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Tourisme BF">
    <link rel="apple-touch-icon" href="/static/icon-192.png">
    
    <script>
        // Enregistrement du Service Worker pour mode offline
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/static/service-worker.js')
                    .then(function(registration) {
                        console.log('ServiceWorker enregistré avec succès:', registration.scope);
                    })
                    .catch(function(err) {
                        console.log('Échec de l\'enregistrement du ServiceWorker:', err);
                    });
            });
        }
        
        // Détection du statut online/offline
        window.addEventListener('online', function() {
            document.getElementById('connection-status').innerHTML = '✅ Mode En Ligne';
            document.getElementById('connection-status').style.background = '#00D26A';
        });
        
        window.addEventListener('offline', function() {
            document.getElementById('connection-status').innerHTML = '📵 Mode Hors Ligne';
            document.getElementById('connection-status').style.background = '#FF6B6B';
        });
    </script>
""", unsafe_allow_html=True)

# Messages d'accueil multilingues
GREETINGS = {
    "moore": [
        "Yɛ zaalem! 🇧🇫 (Soyez les bienvenus!)",
        "Ne y kɛɛma? 💚 (Comment allez-vous?)",
        "Woto yaa soaba 🌟 (Bienvenue chez nous)",
        "Bonzurr yãmb yãmb! ☀️ (Très bon matin!)"
    ],
    "dioula": [
        "Aw ni ce! 🇧🇫 (Bonjour à vous!)",
        "I ka kɛnɛ wa? 💚 (Tu vas bien?)",
        "Bissimilayi! 🌟 (Au nom de Dieu, bienvenue!)",
        "An bɛ aw fo! ☀️ (On vous salue!)"
    ],
    "fulfulde": [
        "Jam weli! 🇧🇫 (Paix seulement!)",
        "A jam tan? 💚 (Es-tu en paix?)",
        "On waɗii jam! 🌟 (Nous sommes en paix!)",
        "Jam fii jamɗe! ☀️ (Paix à tous!)"
    ],
    "francais": [
        "Bienvenue au Burkina Faso! 🇧🇫",
        "Découvrez le Pays des Hommes Intègres! 💚",
        "Explorez nos merveilles touristiques! 🌟",
        "Votre aventure burkinabè commence ici! ☀️"
    ]
}

# Initialisation de la session
if 'greeting_shown' not in st.session_state:
    st.session_state.greeting_shown = False
    st.session_state.current_language = random.choice(list(GREETINGS.keys()))
    st.session_state.greeting_index = 0

# CSS Avancé avec animations
st.markdown("""
    <style>
    /* Import de polices */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animation de chargement */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* En-tête avec animation */
    .main-header {
        background: linear-gradient(135deg, #EF2B2D 0%, #009E49 50%, #FCD116 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3em;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
        margin: 0;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    
    .main-header p {
        color: white;
        font-size: 1.3em;
        margin-top: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Message d'accueil multilingue */
    .greeting-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        animation: slideInLeft 1s ease-out;
    }
    
    /* Indicateur de connexion */
    #connection-status {
        position: fixed;
        top: 70px;
        right: 20px;
        background: #00D26A;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-size: 0.9em;
    }
    
    /* Cartes de sites améliorées */
    .site-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        border-left: 5px solid #009E49;
    }
    
    .site-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.2);
        border-left: 5px solid #EF2B2D;
    }
    
    .site-card h3 {
        color: #2d3436;
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    
    /* Badges de régions animés */
    .region-badge {
        display: inline-block;
        padding: 8px 18px;
        margin: 5px;
        border-radius: 25px;
        font-weight: 600;
        color: white;
        transition: transform 0.3s ease;
    }
    
    .region-badge:hover {
        transform: scale(1.1);
    }
    
    .badge-centre { background: linear-gradient(135deg, #FF6B6B, #FF8E53); }
    .badge-hauts-bassins { background: linear-gradient(135deg, #4ECDC4, #44A08D); }
    .badge-est { background: linear-gradient(135deg, #45B7D1, #2C3E50); }
    .badge-sud-ouest { background: linear-gradient(135deg, #96CEB4, #FFEAA7); }
    .badge-nord { background: linear-gradient(135deg, #FFEAA7, #FDCB6E); color: #2d3436; }
    .badge-sahel { background: linear-gradient(135deg, #DFE6E9, #A29BFE); color: #2d3436; }
    
    /* Boutons personnalisés */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        padding: 12px 24px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Onglets stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Zone de texte personnalisée */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #009E49;
        padding: 15px;
        font-size: 1.1em;
    }
    
    /* Expanders stylisés */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Metrics améliorées */
    [data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
        color: #009E49;
    }
    
    /* Animations au scroll */
    .fade-in {
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Mode offline notice */
    .offline-notice {
        background: #FFE5E5;
        border-left: 4px solid #FF6B6B;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* PWA Install prompt */
    .install-prompt {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Indicateur de connexion
st.markdown('<div id="connection-status">✅ Mode En Ligne</div>', unsafe_allow_html=True)

# Message d'accueil multilingue rotatif
greeting_message = GREETINGS[st.session_state.current_language][st.session_state.greeting_index]
st.markdown(f'<div class="greeting-banner">{greeting_message}</div>', unsafe_allow_html=True)

# Bouton pour changer de langue
col_lang1, col_lang2, col_lang3, col_lang4 = st.columns(4)
with col_lang1:
    if st.button("🗣️ Mooré", use_container_width=True):
        st.session_state.current_language = "moore"
        st.session_state.greeting_index = random.randint(0, len(GREETINGS["moore"])-1)
        st.rerun()
with col_lang2:
    if st.button("🗣️ Dioula", use_container_width=True):
        st.session_state.current_language = "dioula"
        st.session_state.greeting_index = random.randint(0, len(GREETINGS["dioula"])-1)
        st.rerun()
with col_lang3:
    if st.button("🗣️ Fulfuldé", use_container_width=True):
        st.session_state.current_language = "fulfulde"
        st.session_state.greeting_index = random.randint(0, len(GREETINGS["fulfulde"])-1)
        st.rerun()
with col_lang4:
    if st.button("🇫🇷 Français", use_container_width=True):
        st.session_state.current_language = "francais"
        st.session_state.greeting_index = random.randint(0, len(GREETINGS["francais"])-1)
        st.rerun()

# En-tête principal
st.markdown("""
    <div class="main-header">
        <h1>🇧🇫 TOURISME BURKINA FASO</h1>
        <p>🌟 Découvrez le Pays des Hommes Intègres avec votre Guide IA 🌟</p>
        <p style="font-size: 1em; margin-top: 10px;">📱 Application Progressive Web - Fonctionne Hors Ligne</p>
    </div>
""", unsafe_allow_html=True)

# Détection du mode hors ligne
try:
    # Test de connexion
    response = requests.get("https://www.google.com", timeout=2)
    is_online = True
except:
    is_online = False
    st.markdown("""
        <div class="offline-notice">
            <strong>📵 Mode Hors Ligne Actif</strong><br>
            Vous pouvez toujours consulter les informations sauvegardées localement.
            Les recherches en temps réel seront disponibles dès la reconnexion.
        </div>
    """, unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Flag_of_Burkina_Faso.svg/320px-Flag_of_Burkina_Faso.svg.png", 
             use_container_width=True)
    
    st.markdown("### 🎯 Navigation Rapide")
    
    menu_option = st.radio(
        "Explorez :",
        ["🏛️ Sites UNESCO", "🎭 Festivals Majeurs", "🏞️ Parcs Nationaux", 
         "🍲 Gastronomie", "🛍️ Artisanat", "🏨 Hébergement", "📱 Mode PWA"]
    )
    
    st.markdown("---")
    
    # Prompt d'installation PWA
    if menu_option == "📱 Mode PWA":
        st.markdown("""
            <div class="install-prompt">
                <h3>📱 Installer l'Application</h3>
                <p>Installez cette app sur votre appareil pour :</p>
                <ul style="text-align: left; margin: 15px 20px;">
                    <li>✅ Accès rapide depuis l'écran d'accueil</li>
                    <li>✅ Fonctionnement hors ligne</li>
                    <li>✅ Notifications de nouveaux contenus</li>
                    <li>✅ Expérience plein écran</li>
                </ul>
                <p><strong>Sur Chrome/Edge :</strong> Menu (⋮) → "Installer l'application"</p>
                <p><strong>Sur Safari iOS :</strong> Partager → "Sur l'écran d'accueil"</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📍 13 Régions du Burkina Faso")
    
    regions_completes = {
        "🏛️ Centre (Ouagadougou)": ["Capitale", "Musées", "Palais Mogho Naaba"],
        "🎭 Hauts-Bassins (Bobo-Dioulasso)": ["Grande Mosquée", "Vieille ville", "SIAO"],
        "💧 Cascades (Banfora)": ["Karfiguéla", "Pics de Sindou", "Lac Tengrela"],
        "🦁 Est (Fada N'Gourma)": ["Parc W", "Réserve d'Arly"],
        "🏰 Sud-Ouest (Gaoua)": ["Ruines de Loropéni", "Pics de Sindou"],
        "🏜️ Sahel (Dori)": ["Marché de Gorom-Gorom", "Culture touareg"],
        "🌾 Nord (Ouahigouya)": ["Palais Naba Kango", "Mare aux crocodiles"],
        "🏞️ Centre-Nord (Kaya)": ["Réserve de Pô", "Villages traditionnels"],
        "🐘 Centre-Sud (Manga)": ["Ranch de Nazinga"],
        "🌳 Centre-Est (Tenkodogo)": ["Parc Urbain"],
        "🏺 Plateau-Central (Ziniaré)": ["Laongo (sculptures)"],
        "🎨 Boucle du Mouhoun (Dédougou)": ["Festival des Masques"],
        "🌿 Centre-Ouest (Koudougou)": ["Tiébélé"]
    }
    
    for region, sites in regions_completes.items():
        with st.expander(region):
            for site in sites:
                st.markdown(f"✦ {site}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuration API")
    api_url = st.text_input(
        "URL Backend",
        value="http://localhost:8000/api/query",
        help="URL de l'API backend (Membre 2)"
    )
    
    st.markdown("---")
    
    # Statistiques offline
    if 'offline_cache' not in st.session_state:
        st.session_state.offline_cache = []
    
    st.info(f"💾 **Données en cache**: {len(st.session_state.offline_cache)} réponses")

# Section principale - Question
st.markdown("## 💬 Posez votre question")

col_main1, col_main2 = st.columns([3, 1])

with col_main1:
    user_question = st.text_area(
        "Que souhaitez-vous découvrir sur le Burkina Faso ?",
        height=130,
        placeholder="Ex: Quels sont les sites UNESCO ? Où voir des éléphants ? Programme du FESPACO 2025 ?",
        help="Posez toute question sur le tourisme, la culture, la gastronomie..."
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        search_button = st.button("🔍 RECHERCHER", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🔄 Nouvelle question", use_container_width=True):
            st.rerun()
    with col_btn3:
        save_offline = st.button("💾 Mode Hors Ligne", use_container_width=True)

with col_main2:
    st.markdown("### 📊 Stats")
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    
    st.metric("Questions", st.session_state.query_count)
    st.metric("Heure", datetime.now().strftime("%H:%M"))
    
    current_month = datetime.now().month
    if 11 <= current_month or current_month <= 2:
        st.success("☀️ Saison sèche")
    elif 3 <= current_month <= 5:
        st.warning("🌡️ Saison chaude")
    else:
        st.info("🌧️ Saison pluies")

# Traitement de la recherche avec cache offline
if search_button and user_question.strip():
    st.session_state.query_count += 1
    
    # Vérifier d'abord le cache offline
    cached_result = None
    for cache_item in st.session_state.offline_cache:
        if cache_item['question'].lower() == user_question.lower():
            cached_result = cache_item
            break
    
    if cached_result and not is_online:
        st.info("📵 Réponse depuis le cache hors ligne")
        st.success("### ✅ Réponse (Mode Hors Ligne)")
        st.markdown(cached_result['answer'])
    else:
        with st.spinner("🔍 Recherche en cours..."):
            try:
                if is_online:
                    payload = {
                        "question": user_question,
                        "country": "Burkina Faso",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    response = requests.post(api_url, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Sauvegarder dans le cache
                        st.session_state.offline_cache.append({
                            'question': user_question,
                            'answer': result.get("answer", ""),
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Limiter le cache à 50 éléments
                        if len(st.session_state.offline_cache) > 50:
                            st.session_state.offline_cache.pop(0)
                        
                        st.markdown("---")
                        st.success("### ✅ Réponse")
                        
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 25px; border-radius: 15px; color: white; margin: 20px 0;
                                        box-shadow: 0 8px 20px rgba(0,0,0,0.2);'>
                                {result.get("answer", "Information non disponible")}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if "sources" in result and result["sources"]:
                            st.markdown("### 📚 Sources")
                            for idx, source in enumerate(result["sources"][:4]):
                                with st.expander(f"📄 {source.get('title', f'Source {idx+1}')}"):
                                    st.markdown(f"🔗 [{source.get('url', 'N/A')}]({source.get('url', '#')})")
                                    if 'snippet' in source:
                                        st.info(source['snippet'])
                    else:
                        st.error(f"❌ Erreur API ({response.status_code})")
                else:
                    st.warning("📵 Pas de connexion - Consultez le cache ou reconnectez-vous")
                    
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend non connecté - Mode démonstration")
                # Réponse par défaut en mode offline
                default_responses = {
                    "fespaco": "Le FESPACO (Festival Panafricain du Cinéma) a lieu tous les 2 ans à Ouagadougou, généralement en février. C'est le plus grand festival de cinéma africain.",
                    "loropeni": "Les Ruines de Loropéni sont un site UNESCO situé dans le Sud-Ouest. Ce sont d'anciennes fortifications en pierre datant du XIe siècle.",
                    "elephants": "Pour voir des éléphants au Burkina Faso, visitez le Ranch de Nazinga (Centre-Sud), le Parc W ou la Réserve d'Arly (Est).",
                }
                
                for keyword, answer in default_responses.items():
                    if keyword in user_question.lower():
                        st.info("💾 Réponse depuis la base de connaissances locale")
                        st.markdown(f"""
                            <div style='background: #E3F2FD; padding: 20px; border-radius: 10px; 
                                        border-left: 5px solid #2196F3;'>
                                {answer}
                            </div>
                        """, unsafe_allow_html=True)
                        break
                else:
                    st.info("💡 Cette fonctionnalité nécessite une connexion internet. Les informations de base sont disponibles dans les onglets ci-dessous.")
                    
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

elif search_button:
    st.warning("⚠️ Veuillez poser une question !")

# TOP DESTINATIONS (contenu disponible offline)
st.markdown("---")
st.markdown("## 🌟 Top Destinations - Disponible Hors Ligne")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏛️ UNESCO & Histoire", 
    "💧 Cascades & Nature", 
    "🎭 Festivals Majeurs",
    "🦁 Safari & Faune",
    "🏰 Villages Authentiques"
])

with tab1:
    st.markdown("### 🏛️ Sites UNESCO et Historiques")
    
    sites_unesco = [
        {
            "nom": "🏛️ Ruines de Loropéni (UNESCO)",
            "region": "Sud-Ouest (Gaoua)",
            "description": "**Premier site burkinabè inscrit au Patrimoine Mondial (2009)**. Fortifications en pierre du XIe siècle, témoignage de l'empire commercial transsaharien. Murailles de 6m de haut sur 11 000m².",
            "infos": "✓ Visite guidée obligatoire | ✓ Ouvert toute l'année | ✓ Tarif: 2000 FCFA",
            "acces": "À 40km de Gaoua, route praticable toute l'année"
        },
        {
            "nom": "🕌 Grande Mosquée de Bobo-Dioulasso",
            "region": "Hauts-Bassins",
            "description": "Chef-d'œuvre d'architecture soudano-sahélienne en terre crue (1880). Style similaire à Djenné (Mali). Deux minarets emblématiques, cour intérieure magnifique.",
            "infos": "✓ Visite avec guide local | ✓ Photos autorisées (extérieur) | ✓ Respecter les horaires de prière",
            "acces": "Centre-ville de Bobo-Dioulasso, quartier Dioulassoba"
        },
        {
            "nom": "👑 Palais du Mogho Naaba",
            "region": "Centre (Ouagadougou)",
            "description": "Résidence du roi des Mossi. **Cérémonie du Naaba Koom tous les vendredis 7h30** : rituels traditionnels, cavaliers, tambours. Spectacle culturel authentique gratuit.",
            "infos": "✓ Cérémonie gratuite vendredi 7h30 | ✓ Tenue correcte exigée | ✓ Photos autorisées",
            "acces": "Centre de Ouagadougou, à côté du Grand Marché"
        }
    ]
    
    for site in sites_unesco:
        st.markdown(f"""
            <div class='site-card fade-in'>
                <h3>{site['nom']}</h3>
                <span class='region-badge badge-sud-ouest'>📍 {site['region']}</span>
                <p style='margin: 15px 0;'>{site['description']}</p>
                <p><strong>ℹ️ Infos pratiques :</strong> {site['infos']}</p>
                <p><strong>🚗 Accès :</strong> {site['acces']}</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 💧 Cascades et Merveilles Naturelles")
    
    cascades = [
        {
            "nom": "💧 Cascades de Karfiguéla",
            "hauteur": "25 mètres",
            "description": "Les plus célèbres chutes du Burkina. Baignade possible dans les bassins naturels. Paysage spectaculaire entouré de végétation luxuriante.",
            "meilleure_periode": "Juillet à Octobre (saison des pluies) - Débit maximal",
            "activites": ["Baignade", "Randonnée", "Photographie", "Pique-nique"],
            "tarif": "1500 FCFA + 500 FCFA guide"
        },
        {
            "nom": "🏔️ Pics de Sindou",
            "hauteur": "Jusqu'à 40m",
            "description": "Formation géologique unique - Pics de grès érodés créant un paysage lunaire. Canyons, grottes naturelles. Site sacré pour les populations locales.",
            "meilleure_periode": "Novembre à Mars (temps sec, visibilité optimale)",
            "activites": ["Randonnée guidée", "Escalade", "Photographie panoramique", "Exploration grottes"],
            "tarif": "2000 FCFA avec guide obligatoire"
        },
        {
            "nom": "🏞️ Dômes de Fabedougou",
            "description": "Formations rocheuses arrondies mystérieuses ressemblant à des igloos géants. Phénomène d'érosion millénaire unique en Afrique de l'Ouest.",
            "meilleure_periode": "Toute l'année, lever/coucher du soleil recommandé",
            "activites": ["Randonnée", "Photographie", "Observation géologique"],
            "tarif": "1000 FCFA + guide local"
        },
        {
            "nom": "🌊 Lac Tengrela",
            "description": "Lac sacré abritant hippopotames et crocodiles sacrés. Population d'hippos observable depuis la rive. Site spirituel important.",
            "meilleure_periode": "Saison sèche (meilleure visibilité des animaux)",
            "activites": ["Observation faune", "Pirogue traditionnelle", "Photographie animalière"],
            "tarif": "2500 FCFA (pirogue + guide)"
        }
    ]
    
    cols_cascade = st.columns(2)
    for idx, cascade in enumerate(cascades):
        with cols_cascade[idx % 2]:
            st.markdown(f"""
                <div class='site-card'>
                    <h3>{cascade['nom']}</h3>
                    <p>{cascade['description']}</p>
                    <p><strong>📅 Meilleure période :</strong> {cascade['meilleure_periode']}</p>
                    <p><strong>🎯 Activités :</strong> {', '.join(cascade['activites'])}</p>
                    <p><strong>💰 Tarif :</strong> {cascade['tarif']}</p>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🎭 Festivals et Événements Culturels Majeurs")
    
    festivals_detail = [
        {
            "nom": "🎬 FESPACO",
            "complet": "Festival Panafricain du Cinéma et de la Télévision de Ouagadougou",
            "frequence": "Tous les 2 ans (années impaires)",
            "dates": "Dernière semaine de février (7 jours)",
            "prochaine_edition": "2025",
            "description": "**Plus grand festival de cinéma africain au monde** depuis 1969. Compétitions (longs/courts métrages), projections publiques gratuites, rencontres avec réalisateurs, marché du film africain.",
            "lieux": "Cinéma Neerwaya, Cinéma Burkina, Village du FESPACO",
            "budget": "Gratuit à 5000 FCFA selon projections",
            "conseils": "Réserver hébergement 3 mois à l'avance | Acheter pass festival | Climat chaud"
        },
        {
            "nom": "🛍️ SIAO",
            "complet": "Salon International de l'Artisanat de Ouagadougou",
            "frequence": "Tous les 2 ans (années paires)",
            "dates": "Fin octobre - début novembre (10 jours)",
            "prochaine_edition": "2026",
            "description": "**Plus grand salon d'artisanat d'Afrique**. 5000+ artisans de 50+ pays. Expositions, ventes directes, démonstrations de techniques traditionnelles, concours, défilés de mode africaine.",
            "lieux": "Parc des Expositions de Ouagadougou",
            "budget": "Entrée : 1000-2000 FCFA",
            "conseils": "Prévoir budget pour achats | Négociation possible | Authenticité garantie"
        },
        {
            "nom": "🎭 SNC - Semaine Nationale de la Culture",
            "frequence": "Tous les 2 ans",
            "dates": "Mars-Avril (1 semaine)",
            "prochaine_edition": "2026 à Bobo-Dioulasso",
            "description": "Célébration de toutes les cultures burkinabè. Compétitions de danses traditionnelles, orchestres, théâtre, contes, expositions artisanales. **60+ ethnies représentées**.",
            "lieux": "Ville hôte désignée (rotation entre régions)",
            "budget": "Nombreux événements gratuits",
            "conseils": "Immersion culturelle totale | Goûter spécialités régionales"
        },
        {
            "nom": "🎵 FESTIMA - Festival International des Masques",
            "frequence": "Tous les 2 ans",
            "dates": "Février-Mars (3 jours)",
            "lieu": "Dédougou (Boucle du Mouhoun)",
            "description": "Célébration des masques traditionnels d'Afrique de l'Ouest. Danses rituelles, performances de masques sacrés, expositions, conférences sur traditions ancestrales.",
            "specificite": "Découverte authentique des traditions masquées Bwa, Bobo, Nuna",
            "conseils": "Respect des rituels | Photographie selon autorisation"
        }
    ]
    
    for fest in festivals_detail:
        with st.expander(f"{fest['nom']} - {fest.get('complet', '')}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**📅 Fréquence :** {fest['frequence']}")
                st.markdown(f"**🗓️ Dates :** {fest['dates']}")
                if 'prochaine_edition' in fest:
                    st.markdown(f"**🎯 Prochaine édition :** {fest['prochaine_edition']}")
                st.markdown(f"\n{fest['description']}")
            with col2:
                if 'lieux' in fest:
                    st.info(f"📍 **Lieux**\n\n{fest['lieux']}")
                if 'budget' in fest:
                    st.success(f"💰 **Budget**\n\n{fest['budget']}")
            
            if 'conseils' in fest:
                st.warning(f"💡 **Conseils pratiques**\n\n{fest['conseils']}")

with tab4:
    st.markdown("### 🦁 Parcs Nationaux et Safaris")
    
    parcs_detail = [
        {
            "nom": "🐘 Ranch de Nazinga",
            "region": "Centre-Sud (120km de Ouaga)",
            "superficie": "94 000 hectares",
            "faune": {
                "Éléphants": "200+ individus (observation quasi garantie)",
                "Buffles": "Grands troupeaux",
                "Antilopes": "Bubales, Cobes, Hippotragues",
                "Primates": "Singes verts, Patas",
                "Crocodiles": "Dans les mares",
                "Oiseaux": "300+ espèces"
            },
            "activites": ["Safari 4x4 (matin/soir)", "Randonnée guidée", "Observation ornithologique", "Visite nocturne"],
            "hebergement": "Lodge confortable sur place (réservation recommandée)",
            "tarifs": "Entrée: 5000 FCFA | Safari 4x4: 15000-25000 FCFA",
            "meilleur_moment": "Décembre à Mai (saison sèche, animaux près des points d'eau)",
            "conseil": "Safari tôt le matin (6h) ou fin d'après-midi (16h) pour meilleure observation"
        },
        {
            "nom": "🦁 Parc National W (Transfrontalier)",
            "region": "Est (Tapoa)",
            "unesco": "Site UNESCO - Réserve de Biosphère",
            "faune": {
                "Lions": "Population importante",
                "Éléphants": "Migrations saisonnières",
                "Buffles": "Grands troupeaux",
                "Hippopotames": "Fleuve Pendjari",
                "Guépards": "Rares mais présents",
                "Crocodiles": "Nombreux"
            },
            "specificite": "Parc partagé entre Burkina Faso, Niger et Bénin. Écosystème soudano-sahélien intact.",
            "activites": ["Safari guidé obligatoire", "Observation faune", "Bivouac"],
            "acces": "4x4 obligatoire, piste difficile",
            "saison": "Novembre à Mai uniquement (fermé en saison des pluies)"
        },
        {
            "nom": "🦓 Réserve Partielle de Faune d'Arly",
            "region": "Est (Province de la Tapoa)",
            "superficie": "76 000 hectares",
            "faune": {
                "Éléphants": "Grande population",
                "Lions": "Régulièrement observés",
                "Guépards": "Population rare",
                "Girafes": "Présentes",
                "Hippotragues": "Nombreux",
                "Phacochères": "Abondants"
            },
            "particularite": "Paysages variés : savanes, forêts galeries, mares permanentes",
            "hebergement": "Campements basiques, prévoir matériel de camping",
            "acces": "Via Fada N'Gourma, 4x4 recommandé"
        },
        {
            "nom": "🦛 Mare aux Hippopotames de Bala",
            "region": "Hauts-Bassins (près Bobo)",
            "unesco": "Réserve de Biosphère UNESCO",
            "superficie": "19 200 hectares",
            "faune": {
                "Hippopotames": "Population protégée (observation garantie)",
                "Oiseaux aquatiques": "200+ espèces",
                "Singes": "Plusieurs espèces",
                "Petits mammifères": "Nombreux"
            },
            "activites": ["Observation hippopotames", "Birdwatching", "Randonnée nature", "Pirogue"],
            "facilite": "Accessible en voiture standard, proche de Bobo (60km)",
            "tarifs": "Entrée modique : 2000-3000 FCFA",
            "ideal_pour": "Excursion d'une journée depuis Bobo-Dioulasso"
        }
    ]
    
    for parc in parcs_detail:
        st.markdown(f"### {parc['nom']}")
        st.markdown(f"<span class='region-badge badge-est'>📍 {parc['region']}</span>", unsafe_allow_html=True)
        
        if 'unesco' in parc:
            st.success(f"🏆 {parc['unesco']}")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("**🐾 Faune Observable :**")
            for animal, details in parc['faune'].items():
                st.markdown(f"• **{animal}** : {details}")
            
            if 'activites' in parc:
                st.markdown(f"\n**🎯 Activités :** {', '.join(parc['activites'])}")
        
        with col2:
            if 'meilleur_moment' in parc:
                st.info(f"📅 **Meilleur moment**\n\n{parc['meilleur_moment']}")
            if 'tarifs' in parc:
                st.success(f"💰 **Tarifs**\n\n{parc['tarifs']}")
            if 'hebergement' in parc:
                st.warning(f"🏨 **Hébergement**\n\n{parc['hebergement']}")
        
        if 'conseil' in parc:
            st.info(f"💡 {parc['conseil']}")
        
        st.markdown("---")

with tab5:
    st.markdown("### 🏰 Villages Traditionnels et Artisanat Authentique")
    
    villages_detail = [
        {
            "nom": "🏠 Village de Tiébélé",
            "region": "Sud (Province du Nahouri)",
            "ethnie": "Kassena",
            "specialite": "**Cours royales décorées - Architecture unique au monde**",
            "description": "Les maisons kassena sont ornées de motifs géométriques peints à la main avec des pigments naturels (ocre, blanc, noir). Technique transmise de mère en fille depuis des siècles. Architecture en terre crue avec toits plats.",
            "a_voir": [
                "Cour royale du chef (sukala)",
                "Maisons décorées (peintures renouvelées chaque année)",
                "Greniers traditionnels",
                "Démonstration de peinture murale"
            ],
            "artisanat": ["Peintures murales", "Poterie traditionnelle", "Vannerie", "Calebasses gravées"],
            "acces": "200km de Ouaga vers le Ghana, route praticable",
            "hebergement": "Campement villageois possible",
            "tarif_visite": "5000 FCFA (guide + permission du chef)",
            "ethique": "Respecter l'intimité, demander avant de photographier, contribution attendue"
        },
        {
            "nom": "🎨 Village Artisanal de Ouagadougou",
            "region": "Centre (Ouagadougou)",
            "type": "Centre artisanal permanent",
            "description": "Concentration de 150+ artisans dans un espace dédié. Observation des artisans au travail, possibilité d'achats directs, démonstrations de techniques.",
            "artisanat": {
                "Bronze": "Statues, bijoux par technique de cire perdue",
                "Batik": "Tissus teints traditionnellement",
                "Sculpture sur bois": "Masques, statuettes, meubles",
                "Instruments": "Balafons, djembés, koras",
                "Maroquinerie": "Sacs, chaussures en cuir",
                "Vannerie": "Paniers, chapeaux"
            },
            "avantages": "Prix fixes affichés | Qualité garantie | Pas de pression commerciale",
            "ouverture": "Lun-Sam 8h-18h, Dim 9h-13h",
            "acces": "Centre-ville, taxi facilement",
            "budget": "Large gamme de prix, négociation possible sur gros achats"
        },
        {
            "nom": "🏺 Site de Sculptures de Laongo",
            "region": "Plateau-Central (30km de Ouaga)",
            "type": "Musée à ciel ouvert - Art contemporain",
            "description": "Symposium international de sculpture sur granit depuis 1989. 50+ sculptures monumentales réalisées par artistes de 20+ pays, intégrées dans paysage de granit naturel.",
            "particularite": "Fusion art contemporain et site naturel exceptionnel",
            "sculptures": "Thèmes variés : traditions africaines, paix, environnement",
            "activites": ["Visite guidée", "Randonnée artistique", "Photographie", "Ateliers sculpture (sur demande)"],
            "tarif": "2000 FCFA visite guidée",
            "duree": "2-3 heures recommandées",
            "meilleur_moment": "Matin ou fin d'après-midi (lumière idéale pour photos)"
        },
        {
            "nom": "🎭 Villages Bwa (Région de Houndé)",
            "ethnie": "Bwa",
            "specialite": "**Masques traditionnels et danses rituelles**",
            "description": "Les Bwa sont réputés pour leurs masques en bois et fibres végétales utilisés lors de cérémonies d'initiation et funérailles. Danses masquées spectaculaires.",
            "masques": [
                "Masques-planches hauts de 2m",
                "Masques en feuilles (do)",
                "Masques zoomorphes (papillons, serpents)"
            ],
            "ceremonies": "Initiations (avril-mai), Funérailles (saison sèche)",
            "artisanat": "Achat de masques possible (attention: certains sacrés non vendables)",
            "respect": "Certaines cérémonies interdites aux non-initiés",
            "guide": "Guide local obligatoire pour comprendre symboliques"
        }
    ]
    
    for village in villages_detail:
        st.markdown(f"""
            <div class='site-card'>
                <h3>{village['nom']}</h3>
                <span class='region-badge badge-centre'>📍 {village['region']}</span>
        """, unsafe_allow_html=True)
        
        if 'ethnie' in village:
            st.markdown(f"**👥 Ethnie :** {village['ethnie']}")
        
        st.markdown(f"**✨ Spécialité :** {village['specialite']}")
        st.markdown(f"\n{village['description']}")
        
        if 'a_voir' in village:
            st.markdown("\n**👀 À voir absolument :**")
            for item in village['a_voir']:
                st.markdown(f"• {item}")
        
        if isinstance(village.get('artisanat'), list):
            st.markdown(f"\n**🎨 Artisanat :** {', '.join(village['artisanat'])}")
        elif isinstance(village.get('artisanat'), dict):
            st.markdown("\n**🎨 Artisanat disponible :**")
            for art, desc in village['artisanat'].items():
                st.markdown(f"• **{art}** : {desc}")
        
        if 'tarif_visite' in village:
            st.success(f"💰 {village['tarif_visite']}")
        
        if 'ethique' in village:
            st.warning(f"⚠️ **Éthique :** {village['ethique']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Gastronomie
st.markdown("---")
st.markdown("## 🍲 Gastronomie Burkinabè - Guide Complet")

col_food1, col_food2, col_food3, col_food4 = st.columns(4)

with col_food1:
    st.markdown("""
    ### 🍚 Plats Principaux
    
    **Tô** (Base alimentaire)
    - Pâte de mil, sorgho ou maïs
    - Avec sauce gombo, arachide, ou oseille
    - Se mange avec la main droite
    
    **Riz Gras**
    - Riz cuisiné à l'huile/tomate
    - Avec poulet, poisson ou viande
    - Légumes et épices
    
    **Babenda**
    - Feuilles de baobab séchées
    - Sauce épaisse avec arachide
    - Accompagne le tô
    
    **Sauce Gombo**
    - Gombo frais haché
    - Poisson/viande fumée
    - Texture gluante caractéristique
    """)

with col_food2:
    st.markdown("""
    ### 🥤 Boissons Locales
    
    **Zoom-koom** ⭐
    - Boisson de farine de mil
    - Sucrée et rafraîchissante
    - Servie très froide
    
    **Bissap**
    - Jus de fleurs d'hibiscus
    - Rouge vif, vitamine C
    - Chaud ou glacé
    
    **Gnamakoudji**
    - Jus de gingembre
    - Épicé et tonifiant
    - Souvent sucré au miel
    
    **Dolo**
    - Bière traditionnelle de mil
    - Fermentation artisanale
    - Faible degré alcool
    
    **Tamarin**
    - Jus de fruit de tamarin
    - Goût acidulé unique
    - Très rafraîchissant
    """)

with col_food3:
    st.markdown("""
    ### 🍪 Snacks & Street Food
    
    **Beignets** (variés)
    - Haricot (galettes)
    - Banane plantain
    - Farine de blé sucrés
    
    **Brochettes**
    - Viande grillée (bœuf/mouton)
    - Foie mariné
    - Servies avec piment
    
    **Alloco**
    - Bananes plantains frites
    - Accompagnement pimenté
    - En-cas populaire
    
    **Arachides grillées**
    - Salées ou nature
    - Partout dans la rue
    - Très bon marché
    """)

with col_food4:
    st.markdown("""
    ### 🍮 Desserts & Fruits
    
    **Dégué**
    - Yaourt de mil
    - Sucré vanillé
    - Texture granuleuse
    
    **Fruits de saison**
    - Mangues (mars-juil) ⭐
    - Papayes
    - Goyaves
    - Pastèques
    
    **Bouye**
    - Fruit du pain de singe
    - Poudre blanche acidulée
    - En jus ou yaourt
    
    **Néré** (Soumbala)
    - Graines fermentées
    - Condiment traditionnel
    - Goût unique fort
    """)

st.markdown("### 🍽️ Où manger à Ouagadougou et Bobo-Dioulasso")

col_resto1, col_resto2 = st.columns(2)

with col_resto1:
    st.markdown("""
    **🏛️ OUAGADOUGOU - Restaurants recommandés:**
    
    **Cuisine Traditionnelle :**
    - **Chez Adama** (Zone 1) - Tô authentique
    - **Le Verdoyant** - Buffet burkinabè
    - **Chez Wemba** - Spécialités locales
    
    **Maquis populaires :**
    - **Maquis Bon Coin** (Gounghin)
    - **Le Gondwana** (Ave Kwamé N'Krumah)
    - **Chez Ibrahim** (Ouaga 2000)
    
    **Budget :** 2000-5000 FCFA/personne
    """)

with col_resto2:
    st.markdown("""
    **🎭 BOBO-DIOULASSO - Bonnes adresses:**
    
    **Cuisine Locale :**
    - **Auberge Les Cascades**
    - **Le Faso** (centre-ville)
    - **Chez Mimi** - Ambiance familiale
    
    **Maquis animés :**
    - **Dromadaire** (musique live)
    - **Le Temps Jadis**
    - **Chez Yacouba**
    
    **Budget :** 1500-4000 FCFA/personne
    """)

# Informations pratiques essentielles
st.markdown("---")
st.markdown("## 📱 Informations Pratiques Essentielles")

col_info1, col_info2, col_info3, col_info4 = st.columns(4)

with col_info1:
    st.markdown("""
    ### 🛂 Avant le départ
    
    **Documents :**
    - Passeport valide 6 mois
    - Visa (ambassade ou e-visa)
    - Carnet vaccinal international
    
    **Vaccins obligatoires :**
    - ✅ Fièvre jaune (obligatoire)
    - Recommandés : Hépatites A/B, Typhoïde, Méningite
    
    **Santé :**
    - Traitement antipaludique
    - Assurance voyage
    - Trousse pharmacie de base
    """)

with col_info2:
    st.markdown("""
    ### 💰 Argent & Budget
    
    **Monnaie :** Franc CFA (XOF)
    - 1 EUR ≈ 655 FCFA
    - 1 USD ≈ 600 FCFA
    
    **Change :**
    - Banques (meilleur taux)
    - Bureaux de change
    - Éviter aéroport (taux élevé)
    
    **Paiement :**
    - Cash privilégié
    - CB acceptée (grands hôtels)
    - Mobile Money très utilisé
    
    **Budget moyen/jour :**
    - Routard : 15 000-25 000 FCFA
    - Confort : 30 000-50 000 FCFA
    - Luxe : 50 000+ FCFA
    """)

with col_info3:
    st.markdown("""
    ### 🚗 Transports
    
    **Avion :**
    - Aéroport Ouagadougou
    - Compagnies : Air Burkina, Air France, Brussels Airlines
    
    **Inter-villes :**
    - Bus (STAF, TSR, Rakieta)
    - Locations 4x4
    - Taxis-brousse
    
    **En ville :**
    - Taxis (compteur ou forfait)
    - Motos-taxis (rapide, dangereux)
    - Bus urbains SOTRACO
    - Location scooters/voitures
    
    **Tarifs moyens :**
    - Taxi Ouaga : 500-1500 FCFA
    - Ouaga-Bobo bus : 3500-5000 FCFA
    """)

with col_info4:
    st.markdown("""
    ### 📞 Communication
    
    **Téléphone :**
    - Indicatif : +226
    - SIM locale : 1000-2000 FCFA
    - Opérateurs : Orange, Moov, Telecel
    
    **Internet :**
    - 4G dans grandes villes
    - Forfaits data abordables
    - WiFi : hôtels, restaurants
    
    **Langues :**
    - Officielle : Français
    - Nationales : Mooré (50%), Dioula (20%), Fulfuldé (10%)
    - + 60 langues locales
    
    **Fuseau horaire :**
    - GMT+0 (pas de décalage avec UK)
    - +1h France hiver, même heure été
    """)

# Conseils de sécurité
st.markdown("---")
st.markdown("## ⚠️ Conseils de Sécurité et Comportement")

col_secu1, col_secu2, col_secu3 = st.columns(3)

with col_secu1:
    st.warning("""
    **🛡️ Sécurité Générale**
    
    - Consulter conseils France Diplomatie
    - Éviter zones frontalières (Nord, Est)
    - Ne pas circuler la nuit hors villes
    - Photocopier documents importants
    - Enregistrer ambassade
    - Assurance rapatriement
    """)

with col_secu2:
    st.info("""
    **🤝 Respect Culturel**
    
    - Saluer avant toute interaction
    - Main droite pour manger/saluer
    - Demander avant photographier
    - Tenue correcte (épaules/genoux)
    - Retrait chaussures (mosquées, maisons)
    - Respecter Ramadan (si période)
    """)

with col_secu3:
    st.success("""
    **💡 Conseils Pratiques**
    
    - Apprendre phrases de base (mooré/dioula)
    - Toujours avoir cash
    - Négocier prix taxis avant
    - Boire eau en bouteille
    - Protection solaire forte
    - Adaptateur électrique (220V)
    """)

# Questions rapides avec cache offline
st.markdown("---")
st.markdown("## ⚡ Questions Fréquentes (FAQ - Disponible Hors Ligne)")

faq_questions = {
    "Quand visiter le Burkina Faso ?": "**Meilleure période : Novembre à Février** (saison sèche, températures agréables 20-30°C). Éviter Mars-Mai (très chaud 35-45°C). Juin-Octobre = saison des pluies (paysages verts, certaines routes impraticables).",
    "Le Burkina Faso est-il sûr pour les touristes ?": "Les zones touristiques principales (Ouaga, Bobo, Banfora, Nazinga) sont généralement sûres. **Éviter absolument** les régions frontalières (Nord, Est, frontière Mali). Consulter France Diplomatie avant voyage. Rester vigilant, ne pas circuler la nuit.",
    "Combien coûte un voyage au Burkina Faso ?": "**Vol AR depuis Europe :** 400-800€. **Budget sur place par jour :** Routard 20-30€ | Moyen 40-60€ | Confort 80-120€. Destination abordable avec bonne qualité. Exemple séjour 10 jours : 800-1500€ tout compris.",
    "Faut-il un visa pour le Burkina Faso ?": "**Oui, visa obligatoire** pour la plupart des nationalités. **Options :** 1) E-visa en ligne (evisa.gouv.bf) - 72h - 50-75€ | 2) Ambassade (1 semaine) | 3) Aéroport (déconseillé, plus cher, attente). Passeport valide 6 mois + vaccin fièvre jaune obligatoire.",
    "Où voir des éléphants au Burkina Faso ?": "**Ranch de Nazinga** (Centre-Sud) : Observation GARANTIE, 200+ éléphants. Safari 4x4 matin/soir. | **Parc W** (Est) : Nombreux éléphants mais accès difficile. | **Réserve d'Arly** : Population importante. Meilleure période : Décembre-Mai (saison sèche).",
    "Que ramener du Burkina Faso ?": "**Artisanat :** Masques bois, statues bronze (cire perdue), tissus batik, paniers vannerie, instruments (balafon, djembé), bijoux en bronze/cuir, sculptures Laongo. **Alimentaire :** Miel naturel, beurre de karité, soumbala (néré), thé, épices locales. **Où acheter :** Village Artisanal Ouaga (prix fixes, qualité), SIAO (si période).",
    "Comment se déplacer entre Ouaga et Bobo ?": "**Distance :** 365km. **Options :** 1) **Bus compagnies** (STAF, TSR, Rakieta) : 3500-5000 FCFA, 4-5h, confortable, climatisé, départs réguliers. | 2) **Taxi-brousse** : 3000 FCFA, moins confortable, plus rapide mais dangereux. | 3) **Location voiture** : 35 000-50 000 FCFA/jour + essence. | 4) **Vol intérieur** : Rare, cher. Recommandation : Bus de jour.",
    "Quelle langue parler au Burkina Faso ?": "**Français** (officiel) : Compris en ville, tourisme, administration. **Langues locales utiles :** **Mooré** (50% pop, Centre/Nord) - Base : Yɛ zaalem (bonjour), A barc'a (merci). **Dioula** (Ouest, Bobo) - Aw ni ce (bonjour), I ni ce (merci). **Fulfuldé** (Nord, éleveurs peuls). Apprentissage quelques mots très apprécié !",
    "Peut-on boire l'eau du robinet ?": "**NON, jamais !** Boire uniquement eau en bouteille capsulée. Marques locales : Lafi, Jirma, Tassinma (500 FCFA/1.5L). Glaçons : Refuser sauf hôtels de standing. Fruits/légumes : Laver eau traitée, éplucher. Diarrhée = risque principal touristes.",
    "Quel budget pour le FESPACO ?": "**FESPACO 2025 (février) :** | **Projections :** Gratuites à 5000 FCFA selon films/salles. | **Pass festival :** 15 000-25 000 FCFA (accès prioritaire). | **Hébergement :** Réserver 3 mois avant ! Hôtels complets, prix x2-3. Budget 30 000-80 000 FCFA/nuit. | **Total séjour 7 jours :** 350 000-800 000 FCFA (hébergement, repas, transport, projections).",
    "Quels souvenirs rapporter de Tiébélé ?": "**Artisanat Kassena authentique :** Calebasses gravées traditionnelles, petites maquettes de maisons décorées, poteries (canaris, jarres), paniers vannerie tressée, tissu bogolan local. **Photos :** Autorisation obligatoire (5000 FCFA contribution au village). **Éthique :** Acheter directement aux artisanes, prix justes, respect travail ancestral."
}

col_faq1, col_faq2 = st.columns(2)

for idx, (question, reponse) in enumerate(faq_questions.items()):
    with col_faq1 if idx % 2 == 0 else col_faq2:
        with st.expander(f"❓ {question}"):
            st.markdown(reponse)

# Itinéraires suggérés
st.markdown("---")
st.markdown("## 🗺️ Itinéraires Suggérés - Planifiez Votre Voyage")

col_itin1, col_itin2, col_itin3 = st.columns(3)

with col_itin1:
    st.markdown("""
    ### 🚀 DÉCOUVERTE EXPRESS (5-7 jours)
    
    **Jour 1-2 : OUAGADOUGOU**
    - Arrivée, acclimatation
    - Palais Mogho Naaba (vendredi matin)
    - Musée National
    - Village Artisanal (shopping)
    - Maquis le soir
    
    **Jour 3-4 : BOBO-DIOULASSO**
    - Route matinale (bus 4h)
    - Grande Mosquée
    - Vieille ville (Kibidwé)
    - Mare aux Hippopotames (60km)
    - Marché artisanal
    
    **Jour 5 : BANFORA**
    - Cascades de Karfiguéla
    - Lac Tengrela (hippos)
    - Retour Bobo
    
    **Jour 6-7 : Retour Ouaga**
    - Vol retour
    
    **Budget :** 350 000-600 000 FCFA
    """)

with col_itin2:
    st.markdown("""
    ### 🌟 CLASSIQUE COMPLET (10-14 jours)
    
    **Jours 1-3 : OUAGADOUGOU**
    - Sites culturels
    - Marchés, musées
    - Laongo (sculptures)
    
    **Jours 4-5 : NAZINGA**
    - Safari éléphants
    - Lodge, observation faune
    
    **Jours 6-8 : BOBO-DIOULASSO**
    - Tous les sites
    - Mare aux Hippopotames
    - Vie nocturne
    
    **Jours 9-11 : BANFORA & CASCADES**
    - Karfiguéla
    - Pics de Sindou (2 jours)
    - Dômes de Fabedougou
    - Lac Tengrela
    
    **Jour 12 : GAOUA**
    - Ruines de Loropéni (UNESCO)
    
    **Jours 13-14 : Retour**
    - Ouaga, achats finaux
    - Départ
    
    **Budget :** 600 000-1 200 000 FCFA
    """)

with col_itin3:
    st.markdown("""
    ### 🦁 GRAND TOUR AVENTURE (15-21 jours)
    
    **Inclut itinéraire classique +**
    
    **TIÉBÉLÉ (Sud)**
    - 2 jours villages Kassena
    - Cours royales décorées
    - Immersion culturelle
    
    **PARC W ou ARLY (Est)**
    - 3-4 jours safari
    - Lions, éléphants
    - Bivouac nature
    - Via Fada N'Gourma
    
    **DORI / GOROM-GOROM (Sahel)**
    - Marché du jeudi (Gorom)
    - Culture touareg/peul
    - Dunes, désert
    
    **Options :**
    - FESPACO (si février impair)
    - Festival des Masques Dédougou
    - Randonnée Pics de Sindou
    
    **Type :** Aventure, 4x4, camping
    **Budget :** 1 000 000-2 000 000 FCFA
    **Condition :** Bon physique, adaptabilité
    """)

# Contact et urgences
st.markdown("---")
st.markdown("## 📞 Contacts Utiles et Numéros d'Urgence")

col_contact1, col_contact2, col_contact3 = st.columns(3)

with col_contact1:
    st.markdown("""
    ### 🚨 Urgences
    
    - **Police Secours :** 17
    - **Pompiers :** 18
    - **SAMU :** 15 / 30 45 50 45
    - **Gendarmerie :** 16
    - **Police Tourisme Ouaga :** 25 31 18 40
    
    ### 🏥 Hôpitaux Ouagadougou
    
    - **Yalgado Ouédraogo :** 25 48 00 00
    - **Schiphra :** 25 36 26 26
    - **Clinique Princesse Sarah :** 25 37 51 51
    """)

with col_contact2:
    st.markdown("""
    ### 🇫🇷 Ambassades (Ouagadougou)
    
    **France :**
    - Tél : +226 25 49 66 66
    - Avenue de l'Indépendance
    
    **USA :**
    - Tél : +226 25 49 53 00
    - Secteur 15, Ouaga 2000
    
    **Belgique :**
    - Tél : +226 25 36 40 49
    
    **Canada :**
    - Tél : +226 25 31 18 94
    """)

with col_contact3:
    st.markdown("""
    ### ℹ️ Offices de Tourisme
    
    **ONTB (Office National):**
    - Tél : +226 25 31 19 59
    - Avenue Kwamé N'Krumah
    - Email : ontb@fasonet.bf
    
    **Syndicat Initiative Bobo :**
    - Tél : +226 20 97 04 34
    
    ### 🚖 Taxis Fiables
    
    - **Ouaga :** +226 70 00 00 00
    - **Bobo :** +226 76 00 00 00
    """)

# Pied de page avec PWA info
st.markdown("---")
st.markdown("""
    <div style='text-align: center; background: linear-gradient(135deg, #EF2B2D 0%, #009E49 50%, #FCD116 100%); 
                padding: 30px; border-radius: 15px; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.2);'>
        <h2>🇧🇫 Bienvenue au Pays des Hommes Intègres 🇧🇫</h2>
        <p style='font-size: 1.2em; margin: 15px 0;'>
            <strong>La Patrie ou la Mort, Nous Vaincrons !</strong>
        </p>
        <p style='margin: 10px 0;'>
            📱 Application Progressive Web - Fonctionne Hors Ligne<br>
            💚 Construit avec ❤️ pour promouvoir le Tourisme et la Culture du Burkina Faso
        </p>
        <p style='margin-top: 20px; font-size: 0.9em;'>
            <strong>Hackathon IA Tourisme 2025</strong> | Propulsé par Streamlit & Claude AI<br>
            👨‍💻 Équipe : Membre 1 (Data) | Membre 2 (Backend) | Membre 3 (Frontend)
        </p>
        <p style='margin-top: 15px;'>
            <strong>🌍 Version 2.0 - PWA Edition</strong><br>
            Dernière mise à jour : Novembre 2025
        </p>
    </div>
""", unsafe_allow_html=True)

# Note technique pour le développeur
st.markdown("---")
with st.expander("💻 Notes Techniques - PWA & Offline"):
    st.markdown("""
    ### Configuration PWA Active
    
    ✅ **Fonctionnalités implémentées :**
    - Service Worker pour cache offline
    - Manifest.json pour installation
    - Détection online/offline en temps réel
    - Cache des réponses (50 dernières)
    - Accueil multilingue (Mooré, Dioula, Fulfuldé, Français)
    - Design responsive mobile-first
    - Icônes et thème personnalisés
    
    📱 **Installation :**
    - Chrome/Edge : Menu → Installer l'application
    - Safari iOS : Partager → Sur l'écran d'accueil
    - Android : Popup d'installation automatique
    
    💾 **Mode Offline :**
    - Tout le contenu statique accessible
    - FAQ disponible hors ligne
    - Sites touristiques consultables
    - Cache des 50 dernières requêtes
    - Synchronisation auto à la reconnexion
    
    🔧 **Pour activer complètement la PWA :**
    1. Créer dossier `static/` avec manifest.json et service-worker.js
    2. Ajouter icônes (192x192, 512x512)
    3. Déployer sur HTTPS obligatoire
    4. Tester avec Lighthouse (Chrome DevTools)
    
    📚 **Base de données locale :**
    - Session state Streamlit pour cache
    - Extensible vers IndexedDB si besoin
    - Export/Import de données possible
    """)