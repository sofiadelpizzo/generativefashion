import re

def leggi_file(percorso_input):
    """
    Legge il contenuto di un file di testo e restituisce le righe come lista di stringhe.
    """
    try:
        with open(percorso_input, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Errore: Il file '{percorso_input}' non è stato trovato.")
        return []

def correggi_spazi_e_punteggiatura(testo):
    """
    Applica regole di espressioni regolari (regex) per inserire spazi corretti:
    - Separazione tra parola minuscola e successiva parola che inizia con maiuscola (es. "abitoHa" -> "abito Ha").
    - Inserimento di uno spazio dopo segni di punteggiatura (. , ; : ! ?) se seguiti da lettere o numeri.
    - Rimozione di eventuali spazi multipli accidentali.
    """
    # Separazione tra lettera minuscola/numero e lettera maiuscola (tipico errore di concatenazione scraping)
    testo = re.sub(r'([a-z0-9àèéìòù])([A-ZÀÈÉÌÒÙ])', r'\1 \2', testo)
    
    # Inserimento dello spazio dopo la punteggiatura se attaccata alla parola successiva
    testo = re.sub(r'([.,;:!?])([a-zA-ZàèéìòùÀÈÉÌÒÙ])', r'\1 \2', testo)
    
    # Pulizia di spazi doppi o multipli creati dalle sostituzioni
    testo = re.sub(r' +', ' ', testo)
    
    return testo.strip()

def filtra_e_pulisci_contenuto(righe):
    """
    Filtra le righe del testo applicando i criteri di pulizia richiesti:
    - Rimozione di copyright e menzioni Condé Nast.
    - Rimozione di contenuti pubblicitari, promozionali e social.
    - Selezione del contenuto strettamente inerente all'abito e all'evento.
    """
    righe_pulite = []
    didascalie_viste = set()
    
    # Parole chiave o pattern da escludere (copyright, pubblicità, promozioni, social)
    pattern_esclusione = [
        r'condé\s*nast',
        r'tutti\s+i\s+diritti',
        r'copyright',
        r'iscriviti\s+alla\s+newsletter',
        r'segui\s+su\s+instagram',
        r'sponsorizzat[oa]',
        r'pubblicità',
        r'acquista\s+ora',
        r'scopri\s+di\s+più',
        r'cookie',
        r'privacy\s+policy'
    ]
    
    # Parole chiave per mantenere paragrafi strettamente inerenti al look/abito/evento
    parole_chiave_pertinenti = [
        "abito", "vestito", "look", "met gala", "design", "stilista", 
        "corsetto", "tessuto", "colore", "dettaglio", "creazione", 
        "moda", "red carpet", "wearing", "indossa", "ha indossato", "pressione", "bolle", "vetro"
    ]
    
    in_intestazione = True

    for riga in righe:
        riga_str = riga.strip()
        
        # Manteniamo la struttura visiva dell'intestazione (titolo e divisori)
        if riga_str.startswith("===") or riga_str.startswith("---") or riga_str.startswith("TITOLO:"):
            righe_pulite.append(riga_str)
            if riga_str.startswith("---"):
                in_intestazione = False
            continue
            
        if not riga_str:
            continue
            
        # 1. Correzione di spazi e punteggiatura
        riga_corretta = correggi_spazi_e_punteggiatura(riga_str)
        riga_lower = riga_corretta.lower()
        
        # 2. Controllo ed eliminazione del Copyright e Pubblicità
        if any(re.search(p, riga_lower) for p in pattern_esclusione):
            continue
            
        # 3. Controllo didascalie ripetitive (evita di inserire duplicati identici)
        if riga_corretta in didascalie_viste:
            continue
        didascalie_viste.add(riga_corretta)
        
        # 4. Filtraggio del contesto (mantiene solo quello riferito all'abito e all'evento principale)
        if not in_intestazione:
            # Manteniamo il paragrafo solo se contiene elementi inerenti all'abito/look/evento
            if any(parola in riga_lower for parola in parole_chiave_pertinenti):
                righe_pulite.append(riga_corretta)
        else:
            righe_pulite.append(riga_corretta)
            
    return righe_pulite

def scrivi_file(percorso_output, righe_pulite):
    """
    Scrive le righe elaborate all'interno del file di output specificato.
    """
    try:
        with open(percorso_output, 'w', encoding='utf-8') as f:
            for riga in righe_pulite:
                f.write(riga + "\n\n")
        print(f"File pulito generato con successo: '{percorso_output}'")
    except IOError as e:
        print(f"Errore durante la scrittura del file '{percorso_output}': {e}")

if __name__ == "__main__":
    # Nomi dei file di input e output
    file_input = "estrazione_articolo1.txt"
    file_output = "articolo1_pulito.txt"
    
    # 1. Lettura del file grezzo
    righe_grezze = leggi_file(file_input)
    
    if righe_grezze:
        # 2. Elaborazione, filtraggio e correzione del testo
        righe_elaborate = filtra_e_pulisci_contenuto(righe_grezze)
        
        # 3. Scrittura del file pulito
        scrivi_file(file_output, righe_elaborate)