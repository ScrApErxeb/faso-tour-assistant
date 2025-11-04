import json
import re
from datetime import datetime

print("=" * 60)
print("🧹 NETTOYAGE ET FUSION DES DONNÉES")
print("=" * 60)

class DataCleaner:
    def __init__(self):
        print("\n[INIT] Initialisation du nettoyeur de données...")
        self.corpus = []
        self.sources = []
        
    def clean_text(self, text):
        """Nettoyer le texte"""
        if not text or not isinstance(text, str):
            return ""
        
        # Enlever les caractères de contrôle
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text)
        
        # Enlever les espaces en début/fin
        text = text.strip()
        
        # Enlever les caractères Unicode bizarres
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        
        return text
    
    def load_json_file(self, filepath):
        """Charger un fichier JSON"""
        try:
            print(f"\n[LOAD] 📂 Chargement: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[LOAD] ✓ {len(data)} documents chargés")
            return data
        except FileNotFoundError:
            print(f"[LOAD] ⚠️ Fichier introuvable: {filepath}")
            return []
        except Exception as e:
            print(f"[LOAD] ✗ Erreur: {str(e)}")
            return []
    
    def merge_data(self):
        """Fusionner les données des deux fichiers"""
        print("\n" + "=" * 60)
        print("🔀 FUSION DES DONNÉES")
        print("=" * 60)
        
        # Charger les données web
        web_data = self.load_json_file('data/raw/web_scraping_raw.json')
        
        # Charger les données PDF
        pdf_data = self.load_json_file('data/raw/pdf_corpus.json')
        
        # Fusionner
        all_data = web_data + pdf_data
        
        print(f"\n[MERGE] 📊 Total avant fusion: {len(all_data)} documents")
        print(f"[MERGE]   • Web: {len(web_data)} documents")
        print(f"[MERGE]   • PDF: {len(pdf_data)} documents")
        
        return all_data
    
    def clean_and_normalize(self, data):
        """Nettoyer et normaliser tous les documents"""
        print("\n" + "=" * 60)
        print("🧼 NETTOYAGE DES DONNÉES")
        print("=" * 60)
        
        cleaned_data = []
        sources_set = set()
        
        for idx, doc in enumerate(data):
            print(f"\r[CLEAN] Document {idx + 1}/{len(data)}...", end='', flush=True)
            
            # Nettoyer les champs texte
            title = self.clean_text(doc.get('title', ''))
            content = self.clean_text(doc.get('content', ''))
            
            # Ignorer les documents vides
            if not content or len(content) < 50:
                continue
            
            # Normaliser la structure
            cleaned_doc = {
                'id': f"doc_{idx + 1:04d}",
                'title': title,
                'content': content,
                'source': doc.get('source', 'Source inconnue'),
                'url': doc.get('url', 'N/A'),
                'type': doc.get('type', 'document'),
                'categorie': doc.get('categorie', 'tourisme'),
                'date_collecte': doc.get('date_collecte', datetime.now().isoformat()),
                'metadata': {
                    'num_pages': doc.get('num_pages', 1),
                    'filename': doc.get('filename', 'N/A'),
                    'content_length': len(content),
                    'word_count': len(content.split())
                }
            }
            
            cleaned_data.append(cleaned_doc)
            
            # Collecter les sources
            source_info = f"{cleaned_doc['source']} - {cleaned_doc['title']} ({cleaned_doc['url']})"
            sources_set.add(source_info)
        
        print(f"\n[CLEAN] ✓ {len(cleaned_data)} documents nettoyés")
        print(f"[CLEAN] ✓ {len(sources_set)} sources uniques")
        
        self.corpus = cleaned_data
        self.sources = sorted(list(sources_set))
        
        return cleaned_data
    
    def calculate_statistics(self):
        """Calculer des statistiques sur le corpus"""
        print("\n" + "=" * 60)
        print("📊 STATISTIQUES DU CORPUS")
        print("=" * 60)
        
        total_docs = len(self.corpus)
        total_chars = sum(doc['metadata']['content_length'] for doc in self.corpus)
        total_words = sum(doc['metadata']['word_count'] for doc in self.corpus)
        total_pages = sum(doc['metadata']['num_pages'] for doc in self.corpus)
        
        # Compter par type
        types_count = {}
        for doc in self.corpus:
            doc_type = doc['type']
            types_count[doc_type] = types_count.get(doc_type, 0) + 1
        
        print(f"\n📈 GLOBAL:")
        print(f"   • Total documents: {total_docs}")
        print(f"   • Total pages: {total_pages}")
        print(f"   • Total caractères: {total_chars:,}")
        print(f"   • Total mots: {total_words:,}")
        print(f"   • Moyenne mots/doc: {total_words // total_docs if total_docs > 0 else 0}")
        
        print(f"\n📋 RÉPARTITION PAR TYPE:")
        for doc_type, count in sorted(types_count.items()):
            print(f"   • {doc_type}: {count} documents")
        
        print(f"\n🔗 SOURCES:")
        print(f"   • {len(self.sources)} sources différentes")
        
        return {
            'total_documents': total_docs,
            'total_pages': total_pages,
            'total_characters': total_chars,
            'total_words': total_words,
            'types_distribution': types_count,
            'num_sources': len(self.sources)
        }
    
    def save_corpus(self):
        """Sauvegarder le corpus final"""
        print("\n" + "=" * 60)
        print("💾 SAUVEGARDE DU CORPUS FINAL")
        print("=" * 60)
        
        # Sauvegarder le corpus
        corpus_file = 'data/corpus.json'
        try:
            with open(corpus_file, 'w', encoding='utf-8') as f:
                json.dump(self.corpus, f, ensure_ascii=False, indent=2)
            print(f"\n[SAVE] ✓ Corpus sauvegardé: {corpus_file}")
        except Exception as e:
            print(f"\n[SAVE] ✗ Erreur sauvegarde corpus: {e}")
    
    def save_sources(self):
        """Sauvegarder la liste des sources"""
        sources_file = 'data/sources.txt'
        try:
            with open(sources_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("SOURCES DU CORPUS - TOURISME BURKINA FASO\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Nombre total de sources: {len(self.sources)}\n\n")
                f.write("=" * 60 + "\n")
                f.write("LISTE DES SOURCES\n")
                f.write("=" * 60 + "\n\n")
                
                for idx, source in enumerate(self.sources, 1):
                    f.write(f"{idx}. {source}\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("FIN DU DOCUMENT\n")
                f.write("=" * 60 + "\n")
            
            print(f"[SAVE] ✓ Sources sauvegardées: {sources_file}")
        except Exception as e:
            print(f"[SAVE] ✗ Erreur sauvegarde sources: {e}")
    
    def save_statistics(self, stats):
        """Sauvegarder les statistiques"""
        stats_file = 'data/statistics.json'
        try:
            stats['date_creation'] = datetime.now().isoformat()
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            print(f"[SAVE] ✓ Statistiques sauvegardées: {stats_file}")
        except Exception as e:
            print(f"[SAVE] ✗ Erreur sauvegarde stats: {e}")

if __name__ == "__main__":
    cleaner = DataCleaner()
    
    # Étape 1: Fusionner les données
    merged_data = cleaner.merge_data()
    
    # Étape 2: Nettoyer et normaliser
    cleaned_data = cleaner.clean_and_normalize(merged_data)
    
    # Étape 3: Calculer les statistiques
    stats = cleaner.calculate_statistics()
    
    # Étape 4: Sauvegarder tout
    cleaner.save_corpus()
    cleaner.save_sources()
    cleaner.save_statistics(stats)
    
    print("\n" + "=" * 60)
    print("✅ NETTOYAGE TERMINÉ")
    print("=" * 60)
    print("\n📁 FICHIERS CRÉÉS:")
    print("   ✓ data/corpus.json")
    print("   ✓ data/sources.txt")
    print("   ✓ data/statistics.json")
    print("\n" + "=" * 60)