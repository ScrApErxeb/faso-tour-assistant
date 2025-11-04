import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

print("=" * 60)
print("DÉBUT DU SCRIPT - DEBUG MODE")
print("=" * 60)

class TourismeBurkinaScraper:
    def __init__(self):
        print("\n[INIT] Initialisation du scraper...")
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            os.makedirs('data/raw', exist_ok=True)
            print("[INIT] ✓ Dossier data/raw créé")
        except Exception as e:
            print(f"[INIT] ✗ Erreur création dossier: {e}")
        
    def scrape_lefaso_tourisme(self):
        """Scraper LeFaso.net - section tourisme/culture"""
        print("\n[LEFASO] Démarrage scraping LeFaso.net...")
        urls = [
            "https://lefaso.net/spip.php?page=recherche&recherche=tourisme",
            "https://lefaso.net/spip.php?page=recherche&recherche=FESPACO",
            "https://lefaso.net/spip.php?page=recherche&recherche=SIAO",
            "https://lefaso.net/spip.php?page=recherche&recherche=culture"
        ]
        
        for url in urls:
            try:
                print(f"[LEFASO] 📰 Scraping: {url}")
                response = requests.get(url, headers=self.headers, timeout=15)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'html.parser')
                
                articles = soup.find_all('div', class_='item') or soup.find_all('article')
                print(f"[LEFASO]   {len(articles)} articles trouvés")
                
                for article in articles[:30]:
                    title_tag = article.find('h3') or article.find('h2') or article.find('a')
                    content_tag = article.find('div', class_='introduction') or article.find('p')
                    
                    if title_tag:
                        title = title_tag.get_text().strip()
                        content = content_tag.get_text().strip() if content_tag else ""
                        link = title_tag.find('a')['href'] if title_tag.find('a') else url
                        
                        self.data.append({
                            'source': 'LeFaso.net',
                            'url': link,
                            'title': title,
                            'content': content,
                            'date_collecte': datetime.now().isoformat(),
                            'type': 'article_presse',
                            'categorie': 'tourisme'
                        })
                
                print(f"[LEFASO]   ✓ {len(articles)} articles traités")
                time.sleep(3)
                
            except Exception as e:
                print(f"[LEFASO]   ✗ Erreur: {str(e)}")
    
    def scrape_burkina24(self):
        """Scraper Burkina24"""
        print("\n[BURKINA24] Démarrage scraping Burkina24...")
        try:
            url = "https://www.burkina24.com/?s=tourisme"
            print(f"[BURKINA24] 📰 URL: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('article', class_='post')
            print(f"[BURKINA24]   {len(articles)} articles trouvés")
            
            for article in articles[:20]:
                title = article.find('h2')
                content = article.find('div', class_='entry-content')
                
                if title:
                    self.data.append({
                        'source': 'Burkina24',
                        'url': url,
                        'title': title.get_text().strip(),
                        'content': content.get_text().strip() if content else "",
                        'date_collecte': datetime.now().isoformat(),
                        'type': 'article_presse',
                        'categorie': 'tourisme'
                    })
            
            print(f"[BURKINA24]   ✓ {len(articles)} articles traités")
            time.sleep(3)
            
        except Exception as e:
            print(f"[BURKINA24]   ✗ Erreur: {str(e)}")
    
    def scrape_wikipedia_tourisme(self):
        """Scraper Wikipedia - pages tourisme Burkina"""
        print("\n[WIKIPEDIA] Démarrage scraping Wikipedia...")
        pages = [
            "https://fr.wikipedia.org/wiki/Tourisme_au_Burkina_Faso",
            "https://fr.wikipedia.org/wiki/Festival_panafricain_du_cinéma_et_de_la_télévision_de_Ouagadougou",
            "https://fr.wikipedia.org/wiki/Salon_international_de_l%27artisanat_de_Ouagadougou",
            "https://fr.wikipedia.org/wiki/Ruines_de_Loropéni",
            "https://fr.wikipedia.org/wiki/Pics_de_Sindou"
        ]
        
        for url in pages:
            try:
                page_name = url.split('/')[-1]
                print(f"[WIKIPEDIA] 📚 Scraping: {page_name}")
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title = soup.find('h1', id='firstHeading')
                content_div = soup.find('div', id='mw-content-text')
                
                if content_div:
                    paragraphs = content_div.find_all('p')
                    text = '\n'.join([p.get_text() for p in paragraphs[:15]])
                    
                    self.data.append({
                        'source': 'Wikipedia',
                        'url': url,
                        'title': title.get_text() if title else 'Article Wikipedia',
                        'content': text,
                        'date_collecte': datetime.now().isoformat(),
                        'type': 'encyclopedie',
                        'categorie': 'tourisme'
                    })
                
                print(f"[WIKIPEDIA]   ✓ Collecté")
                time.sleep(2)
                
            except Exception as e:
                print(f"[WIKIPEDIA]   ✗ Erreur: {str(e)}")
    
    def scrape_unesco_sites(self):
        """Scraper UNESCO - sites Burkina"""
        print("\n[UNESCO] Démarrage scraping UNESCO...")
        try:
            url = "https://whc.unesco.org/en/statesparties/bf"
            print(f"[UNESCO] 🏛️ URL: {url}")
            
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            sites = soup.find_all('li')
            print(f"[UNESCO]   {len(sites)} éléments trouvés")
            
            count = 0
            for site in sites[:10]:
                link = site.find('a')
                if link and 'whc.unesco.org' in str(link.get('href', '')):
                    self.data.append({
                        'source': 'UNESCO',
                        'url': url,
                        'title': link.get_text().strip(),
                        'content': site.get_text().strip(),
                        'date_collecte': datetime.now().isoformat(),
                        'type': 'patrimoine_unesco',
                        'categorie': 'tourisme'
                    })
                    count += 1
            
            print(f"[UNESCO]   ✓ {count} sites collectés")
            time.sleep(2)
            
        except Exception as e:
            print(f"[UNESCO]   ✗ Erreur: {str(e)}")
    
    def add_manual_content(self):
        """Ajouter contenu manuel sur sites touristiques majeurs"""
        print("\n[MANUEL] Ajout de contenu manuel...")
        sites_majeurs = [
            {
                'title': 'FESPACO - Festival Panafricain du Cinéma',
                'content': "Le FESPACO est le plus grand festival de cinéma d'Afrique, organisé tous les deux ans à Ouagadougou depuis 1969. Il attire des cinéastes de tout le continent et du monde entier.",
                'type': 'festival'
            },
            {
                'title': 'SIAO - Salon International de l\'Artisanat',
                'content': "Le SIAO est une vitrine de l'artisanat africain qui se tient à Ouagadougou tous les deux ans. Il rassemble des artisans de toute l'Afrique présentant bronze, tissage, cuir et sculptures.",
                'type': 'festival'
            },
            {
                'title': 'Pics de Sindou',
                'content': "Formation rocheuse spectaculaire dans le sud-ouest du Burkina Faso, les Pics de Sindou sont des formations géologiques en grès sculptées par l'érosion.",
                'type': 'site_naturel'
            },
            {
                'title': 'Cascades de Karfiguéla',
                'content': "Situées près de Banfora, ces cascades sont une attraction touristique majeure pendant la saison des pluies avec leurs chutes d'eau impressionnantes.",
                'type': 'site_naturel'
            },
            {
                'title': 'Ruines de Loropéni',
                'content': "Premier site du Burkina Faso inscrit au patrimoine mondial de l'UNESCO en 2009. Ces ruines fortifiées témoignent du commerce transsaharien de l'or.",
                'type': 'patrimoine_unesco'
            }
        ]
        
        for site in sites_majeurs:
            self.data.append({
                'source': 'Documentation manuelle',
                'url': 'N/A',
                'title': site['title'],
                'content': site['content'],
                'date_collecte': datetime.now().isoformat(),
                'type': site['type'],
                'categorie': 'tourisme'
            })
        
        print(f"[MANUEL] ✓ {len(sites_majeurs)} contenus manuels ajoutés")
    
    def save_data(self):
        """Sauvegarder les données brutes"""
        print("\n[SAVE] Sauvegarde des données...")
        filename = 'data/raw/web_scraping_raw.json'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            
            print(f"[SAVE] ✓ {len(self.data)} documents sauvegardés → {filename}")
            return len(self.data)
        except Exception as e:
            print(f"[SAVE] ✗ Erreur sauvegarde: {e}")
            return 0

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🇧🇫 COLLECTE TOURISME BURKINA FASO")
    print("=" * 60 + "\n")
    
    scraper = TourismeBurkinaScraper()
    
    # Exécuter les scrapings
    scraper.scrape_wikipedia_tourisme()
    scraper.scrape_lefaso_tourisme()
    scraper.scrape_burkina24()
    scraper.scrape_unesco_sites()
    scraper.add_manual_content()
    
    # Sauvegarder
    total = scraper.save_data()
    
    print("\n" + "=" * 60)
    print(f"✅ COLLECTE TERMINÉE: {total} documents")
    print("=" * 60)
    print("\nFIN DU SCRIPT")