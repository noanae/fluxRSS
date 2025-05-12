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

if __name__ == "__main__":
    rss_urls = charger_url()
    keywords = charger_mots_cles()

    print("\nExtrait des flux RSS :")
    print(rss_urls[:2])
    print("\nMots-clés :")
    print(keywords)
