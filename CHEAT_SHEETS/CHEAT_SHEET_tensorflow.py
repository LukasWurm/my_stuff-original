import tensorflow as tf  # Importieren der TensorFlow-Bibliothek

# -------------------------
# Tensoren erstellen
# -------------------------

# Einfache Tensoren erstellen
tensor = tf.constant([[1, 2], [3, 4]])
print(tensor)  # Ausgabe: Tensor mit zwei Dimensionen

# Zufällige Tensoren erstellen
random_tensor = tf.random.normal([3, 3])
print(random_tensor)  # Ausgabe: 3x3-Matrix mit Zufallswerten

# -------------------------
# Einfache neuronale Netze erstellen
# -------------------------

# Neuronales Netz mit Keras API erstellen
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10)
])

# Modell kompilieren
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# -------------------------
# Training eines Modells
# -------------------------

# Beispiel-Daten generieren
data = tf.random.normal([1000, 32])
labels = tf.random.uniform([1000], maxval=10, dtype=tf.int32)

# Modell trainieren
model.fit(data, labels, epochs=10)

# -------------------------
# Modell bewerten
# -------------------------

# Beispiel-Testdaten
test_data = tf.random.normal([100, 32])
test_labels = tf.random.uniform([100], maxval=10, dtype=tf.int32)

# Modell evaluieren
model.evaluate(test_data, test_labels)
