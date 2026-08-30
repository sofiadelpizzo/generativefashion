import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carica le variabili d'ambiente presenti nel file .env
load_dotenv()

def pulisci_testo_con_gemini(file_input_path: str, file_output_path: str):
    """
    Legge un file .txt, lo invia a Gemini per la pulizia e la correzione
    secondo le regole specificate, e salva il risultato in un file .txt.
    """
    # Verifica che la chiave sia stata caricata dal .env
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY non trovata. Assicurati che sia presente nel file .env")

    # 1. Verifica esistenza file di input
    if not os.path.exists(file_input_path):
        raise FileNotFoundError(f"Il file '{file_input_path}' non è stato trovato.")

    # 2. Lettura del file di testo
    print(f"Reading '{file_input_path}'...")
    with open(file_input_path, 'r', encoding='utf-8') as f:
        testo_originale = f.read()

    if not testo_originale.strip():
        print("Il file di input è vuoto.")
        return

    # 3. Definizione delle regole per Gemini
    system_instruction = """
Sei un editor di testo professionale specializzato in articoli di moda e lifestyle.
Il tuo compito è pulire il testo fornito dall'utente applicando le seguenti regole:

1. Tenere solo il contenuto inerente alla descrizione del vestito.
- Rimuovere il contesto dell'evento.
- Il testo deve essere usato per poter dire a un LLM di generare un'immagine basata sulla descrizione del vestito nel testo.

2. Sostituisci eventuali termini che potrebbero essere considerati offensivi o inappropriati con alternative più neutre.

Output richiesto:
Restituisci ESCLUSIVAMENTE il testo pulito, senza commenti, introduzioni, spiegazioni o tag markdown aggiuntivi.

"""

    prompt_utente = f"Ecco il testo da pulire e correggere:\n\n{testo_originale}"

    # 4. Inizializzazione del client (riconosce automaticamente GEMINI_API_KEY dall'ambiente)
    client = genai.Client()

    print("Invio del testo a Gemini per l'elaborazione...")
    
    # 5. Chiamata al modello Gemini
    response = client.models.generate_content(
        # Usa questo modello supportato:
        model='gemini-3.6-flash',
        contents=prompt_utente,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        )
    )

    testo_pulito = response.text

    # 6. Salvataggio del risultato nel file di output
    with open(file_output_path, 'w', encoding='utf-8') as f:
        f.write(testo_pulito)

    print(f"Elaborazione completata! Il file pulito è stato salvato in: '{file_output_path}'")


if __name__ == "__main__":
    INPUT_FILE = "Fase 1/estrazione_articolo2.txt"
    OUTPUT_FILE = "Fase 3/articolo2_ripulito_gemini.txt"

    pulisci_testo_con_gemini(INPUT_FILE, OUTPUT_FILE)