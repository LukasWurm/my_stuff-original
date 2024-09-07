import openai  # Importieren der OpenAI-Bibliothek

# -------------------------
# OpenAI API konfigurieren
# -------------------------

# API-Schlüssel einstellen (API-Key aus Sicherheitsgründen nicht im Code hardcoden)
openai.api_key = 'your-api-key-here'

# -------------------------
# Anfragen an GPT-Modelle
# -------------------------

# Anfrage an GPT-3 oder GPT-4 Modell stellen
response = openai.Completion.create(
    engine="text-davinci-003",  # Verwende "gpt-4" für das neueste GPT-4 Modell
    prompt="Erkläre die Relativitätstheorie",
    max_tokens=100  # Maximale Anzahl an Tokens in der Antwort
)
print(response.choices[0].text.strip())  # Ausgabe der Antwort des Modells

# -------------------------
# Chat-Anfrage an GPT
# -------------------------

# Anfrage an das Chatmodell stellen
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
        {"role": "user", "content": "Was ist Quantenphysik?"}
    ]
)
print(response['choices'][0]['message']['content'])  # Ausgabe der Antwort
