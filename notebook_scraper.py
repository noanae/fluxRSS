import asyncio
import aiohttp
import feedparser
from datetime import datetime

def charger_url(filename="rss_list.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"{len(urls)} flux RSS chargés depuis {filename}")
        return urls
    except FileNotFoundError:
        print(f"Fichier non trouvé : {filename}")
        return []

def charger_mots_cles(filename="mots_cles.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            keywords = [line.strip().lower() for line in f if line.strip()]
        print(f"{len(keywords)} mot(s)-clé(s) chargé(s) depuis {filename}")
        return keywords
    except FileNotFoundError:
        print(f"Fichier non trouvé : {filename}")
        return []

async def recuperer_et_parser(session, url):
    try:
        async with session.get(url) as response:
            content = await response.read()
            feed = feedparser.parse(content)
            print(f"{url}{len(feed.entries)} articles récupérés")
            return feed.entries
    except Exception as e:
        print(f"Erreur sur {url} : {e}")
        return []

async def traiter_flux(rss_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [recuperer_et_parser(session, url) for url in rss_urls]
        all_entries = await asyncio.gather(*tasks)
        return [entry for entries in all_entries for entry in entries] 

def filtrer_par_mots_cles(articles, keywords):
    filtered_articles = []
    for article in articles:
        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()
        for keyword in keywords:
            if keyword in title or keyword in summary:
                filtered_articles.append(article)
                break
    return filtered_articles

def enregistrer_resultats(articles_filtrés, keywords, filename="resultat.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for article in articles_filtrés:
            title = article.get("title", "N/A")
            published = article.get("published", "N/A")
            link = article.get("link", "N/A")
            keywords_found = [
                keyword for keyword in keywords
                if keyword in (article.get("title", "").lower() + article.get("summary", "").lower())
            ]
            for keyword in keywords_found:
                f.write(f"Title: {title}\n")
                f.write(f"Date: {published}\n")
                f.write(f"URL: {link}\n")
                f.write(f"Mot-clé: {keyword}\n")
                f.write("-" * 80 + "\n")
    print(f"{len(articles_filtrés)} article(s) sauvegardé(s) dans {filename}")

if __name__ == "__main__":
    print("\n============ DÉBUT DU TRAITEMENT ============")
    start = datetime.now()

    rss_urls = charger_url("C:/Users/tancr/OneDrive/Bureau/Projet/fluxRSS/rss_list.txt")
    keywords = charger_mots_cles("C:/Users/tancr/OneDrive/Bureau/Projet/fluxRSS/mots_cles.txt")
    
    articles = asyncio.run(traiter_flux(rss_urls))
    print(f"\n{len(articles)} article(s) récupéré(s) au total.")
    articles_filtrés = filtrer_par_mots_cles(articles, keywords)
    print(f"{len(articles_filtrés)} article(s) correspondent aux mots-clés.")
    enregistrer_resultats(articles_filtrés, keywords)
    
    end = datetime.now()
    execution_time = (end - start).total_seconds()
    print("\nTemps d'exécution total :", end - start)
    print(f"Temps d'exécution en secondes : {execution_time:.2f} secondes")
    print("============ FIN DU TRAITEMENT ============\n")
