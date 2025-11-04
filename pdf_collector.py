import requests
import os
import json
from datetime import datetime
import PyPDF2
from io import BytesIO

print("=" * 60)
print("📄 COLLECTE DE PDFs - TOURISME BURKINA FASO")
print("=" * 60)

class PDFTourismeCollector:
    def __init__(self):
        print("\n[INIT] Initialisation du collecteur PDF...")
        self.output_dir = 'data/pdfs'
        self.documents = []
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[INIT] ✓ Dossier {self.output_dir} créé")
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def download_pdf(self, url, filename):
        """Télécharger un PDF"""
        try:
            print(f"\n[DOWNLOAD] 📥 Téléchargement: {filename}")
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content) / 1024  # En KB
                print(f"[DOWNLOAD] ✓ Téléchargé: {file_size:.1f} KB")
                return filepath
            else:
                print(f"[DOWNLOAD] ✗ Erreur HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[DOWNLOAD] ✗ Erreur: {str(e)}")
            return None
    
    def extract_text_from_pdf(self, filepath):
        """Extraire le texte d'un PDF"""
        try:
            print(f"[EXTRACT] 📖 Extraction texte...")
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                
                text = ""
                for page_num, page in enumerate(reader.pages):
                    text += page.extract_text() + "\n"
                
                # Limiter à 50000 caractères pour éviter trop de données
                text = text[:50000]
                
                print(f"[EXTRACT] ✓ {num_pages} pages extraites, {len(text)} caractères")
                return text, num_pages
                
        except Exception as e:
            print(f"[EXTRACT] ✗ Erreur extraction: {str(e)}")
            return "", 0
    
    def collect_official_pdfs(self):
        """Collecter des PDFs officiels sur le tourisme burkinabè"""
        print("\n" + "=" * 60)
        print("🏛️ COLLECTE PDFs OFFICIELS")
        print("=" * 60)
        
        # Liste de PDFs accessibles publiquement
        pdf_sources = [
            {
                'url': 'https://www.ifc.org/content/dam/ifc/doc/2024/ifc-burkina-faso-country-profile-fr.pdf',
                'filename': 'ifc_burkina_faso_profile.pdf',
                'title': 'IFC - Profil Pays Burkina Faso',
                'source': 'IFC/Banque Mondiale'
            },
            {
                'url': 'https://documents1.worldbank.org/curated/en/burkina-faso-tourism.pdf',
                'filename': 'worldbank_burkina_tourism.pdf',
                'title': 'Banque Mondiale - Secteur Touristique Burkina',
                'source': 'Banque Mondiale'
            },
            {
                'url': 'https://www.undp.org/sites/g/files/zskgke326/files/migration/bf/UNDP-BF-Tourism-Study.pdf',
                'filename': 'undp_tourism_burkina.pdf',
                'title': 'PNUD - Étude Tourisme Burkina Faso',
                'source': 'PNUD'
            }
        ]
        
        for source in pdf_sources:
            print(f"\n📄 Source: {source['source']}")
            filepath = self.download_pdf(source['url'], source['filename'])
            
            if filepath and os.path.exists(filepath):
                text, num_pages = self.extract_text_from_pdf(filepath)
                
                if text:
                    self.documents.append({
                        'source': source['source'],
                        'url': source['url'],
                        'title': source['title'],
                        'content': text,
                        'filename': source['filename'],
                        'num_pages': num_pages,
                        'date_collecte': datetime.now().isoformat(),
                        'type': 'rapport_pdf',
                        'categorie': 'tourisme'
                    })
                    print(f"[SUCCESS] ✅ Document ajouté au corpus")
    
    def add_manual_pdf_instructions(self):
        """Instructions pour collecter des PDFs manuellement"""
        print("\n" + "=" * 60)
        print("📝 COLLECTE MANUELLE RECOMMANDÉE")
        print("=" * 60)
        
        manual_sources = {
            "Sites gouvernementaux burkinabè": [
                "Ministère de la Culture et du Tourisme: www.culture.gov.bf",
                "Office National du Tourisme (ONTB): www.ontb.bf",
                "Ministère de l'Économie: www.finances.gov.bf"
            ],
            "Organisations internationales": [
                "UNESCO Burkina: en.unesco.org (chercher 'Burkina Faso')",
                "FAO Documents: www.fao.org/documents (chercher 'Burkina culture')",
                "Banque Africaine de Développement: www.afdb.org",
                "PNUD Burkina: www.undp.org/burkina-faso"
            ],
            "Recherche académique": [
                "Google Scholar: scholar.google.com",
                "  → Rechercher: 'tourisme Burkina Faso filetype:pdf'",
                "  → Rechercher: 'FESPACO culture filetype:pdf'",
                "  → Rechercher: 'patrimoine culturel Mossi filetype:pdf'",
                "  → Rechercher: 'artisanat Bambara filetype:pdf'",
                "ResearchGate: www.researchgate.net",
                "CAIRN: www.cairn.info"
            ],
            "Rapports ONG": [
                "Oxfam Burkina",
                "UNICEF Burkina",
                "Plan International",
                "Care International"
            ]
        }
        
        print("\n🔍 SOURCES RECOMMANDÉES POUR TÉLÉCHARGEMENT MANUEL:\n")
        
        for category, sources in manual_sources.items():
            print(f"\n📌 {category}:")
            for source in sources:
                print(f"   • {source}")
        
        print("\n" + "-" * 60)
        print("💡 CONSEILS:")
        print("   1. Télécharge les PDFs dans le dossier: data/pdfs/")
        print("   2. Nomme-les clairement: ex. 'ontb_rapport_2024.pdf'")
        print("   3. Relance ce script pour extraire le texte")
        print("-" * 60)
    
    def process_existing_pdfs(self):
        """Traiter les PDFs déjà téléchargés dans data/pdfs/"""
        print("\n" + "=" * 60)
        print("📂 TRAITEMENT DES PDFs EXISTANTS")
        print("=" * 60)
        
        pdf_files = [f for f in os.listdir(self.output_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("\n[INFO] Aucun PDF trouvé dans data/pdfs/")
            return
        
        print(f"\n[INFO] {len(pdf_files)} PDF(s) trouvé(s)")
        
        for pdf_file in pdf_files:
            filepath = os.path.join(self.output_dir, pdf_file)
            print(f"\n📄 Traitement: {pdf_file}")
            
            text, num_pages = self.extract_text_from_pdf(filepath)
            
            if text:
                self.documents.append({
                    'source': 'PDF local',
                    'url': 'N/A',
                    'title': pdf_file.replace('.pdf', '').replace('_', ' '),
                    'content': text,
                    'filename': pdf_file,
                    'num_pages': num_pages,
                    'date_collecte': datetime.now().isoformat(),
                    'type': 'rapport_pdf',
                    'categorie': 'tourisme'
                })
                print(f"[SUCCESS] ✅ Ajouté au corpus")
    
    def save_data(self):
        """Sauvegarder les données extraites"""
        print("\n" + "=" * 60)
        print("💾 SAUVEGARDE DES DONNÉES")
        print("=" * 60)
        
        if not self.documents:
            print("\n[WARNING] ⚠️ Aucun document à sauvegarder")
            return 0
        
        filename = 'data/raw/pdf_corpus.json'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            total_pages = sum(doc.get('num_pages', 0) for doc in self.documents)
            total_chars = sum(len(doc.get('content', '')) for doc in self.documents)
            
            print(f"\n[SAVE] ✓ Fichier sauvegardé: {filename}")
            print(f"[SAVE] 📊 {len(self.documents)} documents")
            print(f"[SAVE] 📄 {total_pages} pages totales")
            print(f"[SAVE] 📝 {total_chars:,} caractères")
            
            return len(self.documents)
            
        except Exception as e:
            print(f"[SAVE] ✗ Erreur sauvegarde: {e}")
            return 0

if __name__ == "__main__":
    collector = PDFTourismeCollector()
    
    # Étape 1: Essayer de télécharger des PDFs publics
    collector.collect_official_pdfs()
    
    # Étape 2: Traiter les PDFs déjà téléchargés manuellement
    collector.process_existing_pdfs()
    
    # Étape 3: Afficher instructions pour collecte manuelle
    collector.add_manual_pdf_instructions()
    
    # Étape 4: Sauvegarder
    total = collector.save_data()
    
    print("\n" + "=" * 60)
    print(f"✅ COLLECTE TERMINÉE: {total} documents PDF")
    print("=" * 60)
    print("\n💡 PROCHAINE ÉTAPE:")
    print("   Télécharge manuellement des PDFs et relance ce script")
    print("=" * 60)n