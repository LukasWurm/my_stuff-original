import json  # Importieren der integrierten JSON-Bibliothek

# -------------------------
# JSON lesen
# -------------------------

# Beispiel einer JSON-Datei (String)
json_string = '{"name": "Alice", "age": 30, "city": "Berlin"}'

# JSON-String in ein Python-Dictionary umwandeln
data = json.loads(json_string)
print(data['name'])  # Ausgabe: Alice

# JSON-Datei von Festplatte lesen
with open('data.json', 'r') as file:
    data = json.load(file)
print(data)  # Ausgabe des Inhalts der JSON-Datei

# -------------------------
# JSON schreiben
# -------------------------

# Python-Dictionary in einen JSON-String umwandeln
json_data = json.dumps(data, indent=4)
print(json_data)  # Ausgabe des formatierten JSON-Strings

# Python-Dictionary in eine JSON-Datei schreiben
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)  # Speichern des Dictionarys als JSON-Datei
