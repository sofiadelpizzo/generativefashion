import os
import requests
from bs4 import BeautifulSoup

def estrai_testo_articolo(html_sorgente):
    """
    Analizza il codice HTML di una pagina Vogue Italia ed estrae
    il titolo dell'articolo e tutti i paragrafi di testo significativi.
    
    Parametri:
        html_sorgente (str): Il testo completo del codice HTML.
        
    Ritorna:
        str: Un testo formattato contenente titolo, metadata e paragrafi dell'articolo.
    """
    # Inizializziamo BeautifulSoup per navigare l'albero HTML
    soup = BeautifulSoup(html_sorgente, 'html.parser')
    
    # 1. Estrazione del Titolo (H1) usando la classe reale individuata nell'HTML di Vogue
    titolo_elemento = soup.find('h1', class_='ContentHeaderHed-kobZuw')
    titolo = titolo_elemento.get_text(strip=True) if titolo_elemento else "Titolo non trovato"
    
    # 2. Estrazione del testo dell'articolo (tutti i tag <p>)
    paragrafi = soup.find_all('p')
    testo_estratto = []
    
    # Estraiamo tutti i paragrafi significativi per rendere la funzione generica
    for p in paragrafi:
        testo_paragrafo = p.get_text(strip=True)
        
        # Saltiamo paragrafi vuoti o link correlati standard della redazione ("Leggi anche:")
        if testo_paragrafo and not testo_paragrafo.startswith("Leggi anche:"):
            testo_estratto.append(testo_paragrafo)
            
    # 3. Generazione della struttura del file di testo (.txt)
    linee_testo = [
        "=================================================================",
        f"TITOLO: {titolo}",
        "=================================================================",
        "Dati estratti automaticamente ai fini di ricerca umanistica",
        "-----------------------------------------------------------------\n"
    ]
    
    # Aggiungiamo i paragrafi separati da una riga vuota per migliorarne la leggibilità
    linee_testo.extend([f"{p}\n" for p in testo_estratto])
    
    return "\n".join(linee_testo)


if __name__ == "__main__":
    # --- FASE 1: Richiesta HTTP (Web Scraping Live) ---
    # URL dell'articolo da analizzare (può essere sostituito con qualsiasi URL di Vogue Italia)
    # url_articolo = "https://www.vogue.it/article/eileen-gu-met-gala-2026-look-bubble-dress-di-iris-van-herpen"
    # url_articolo = "https://www.vogue.it/article/hunter-schafer-met-gala-2026-look-prada"
    # url_articolo = "https://www.vogue.it/article/madonna-met-gala-2026-look-gotico-saint-laurent"
    url_articolo = "https://www.vogue.it/article/vittoria-ceretti-met-gala-2026-look-cut-out"

    # Usiamo un User-Agent per simulare un browser ed evitare blocchi di sicurezza
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    
    print(f"Download della pagina in corso: {url_articolo}...")
    
    try:
        # Inviamo la richiesta GET al sito di Vogue
        risposta = requests.get(url_articolo, headers=headers)
        risposta.raise_for_status()  # Genera un errore se la pagina non è raggiungibile
        
        # --- FASE 2: Estrazione e Salvataggio dei Dati ---
        # Chiamiamo la funzione generica passando l'HTML ottenuto
        testo_pulito = estrai_testo_articolo(risposta.text)
        
        # Definiamo il nome del file .txt in cui salvare i risultati
        file_output = "estrazione_articolo4.txt"
        
        # Salviamo la pagina generata come file di testo con codifica adatta ai caratteri accentati (utf-8)
        with open(file_output, "w", encoding="utf-8") as f:
            f.write(testo_pulito)
            
        print(f"Operazione completata! Il testo pulito è stato salvato come: '{file_output}'")
        
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di rete: {e}")