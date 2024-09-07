import numpy as np  # Importiere die NumPy-Bibliothek und nenne sie "np"

# -------------------------
# Grundlegende Array-Erstellung
# -------------------------

# Ein-Dimensionales Array (Vektor)
# Dies ist eine einfache Liste von Zahlen. Ein Vektor hat nur eine Dimension.
a = np.array([1, 2, 3])
print("Ein-Dimensionales Array (Vektor):", a)

# Zwei-Dimensionales Array (Matrix)
# Eine Matrix hat Zeilen und Spalten, also zwei Dimensionen.
b = np.array([[1, 2], [3, 4]])
print("Zwei-Dimensionales Array (Matrix):\n", b)

# Array mit Nullen erstellen
# Dies erzeugt ein 2x3 Array (2 Zeilen, 3 Spalten) gefüllt mit Nullen.
c = np.zeros((2, 3))
print("Array mit Nullen:\n", c)

# Array mit Einsen erstellen
# Dies erzeugt ein 2x3 Array (2 Zeilen, 3 Spalten) gefüllt mit Einsen.
d = np.ones((2, 3))
print("Array mit Einsen:\n", d)

# Array mit einer Folge von Werten
# Erstellt ein Array, das von 0 bis 10 geht, mit einem Schritt von 2 (also [0, 2, 4, 6, 8]).
e = np.arange(0, 10, 2)
print("Array mit einer Folge von Werten:\n", e)

# Array mit gleichmäßig verteilten Werten
# Erstellt ein Array mit 5 gleichmäßig verteilten Werten zwischen 0 und 1.
f = np.linspace(0, 1, 5)
print("Array mit gleichmäßig verteilten Werten:\n", f)

# Identitätsmatrix erstellen
# Eine Identitätsmatrix hat Einsen auf der Hauptdiagonale und Nullen überall sonst.
g = np.eye(3)
print("Identitätsmatrix:\n", g)

# -------------------------
# Array-Operationen
# -------------------------

print("\nArray-Operationen")
# Form und Dimensionen von Arrays
# "shape" gibt die Form (Dimensionen) des Arrays zurück. Hier ist es (2, 2) für 2 Zeilen und 2 Spalten.
print("Form der Matrix:", b.shape)

# Umformen eines Arrays
# "reshape" ändert die Form des Arrays. Hier wird das 2x2 Array in ein 4x1 Array umgeformt.
print("Umgeformte Matrix (4x1):\n", b.reshape((4, 1)))

# Flatten - Array zu einem flachen Array machen
# "flatten" wandelt das Array in ein eindimensionales Array um, unabhängig von der ursprünglichen Form.
print("Flaches Array:", b.flatten())

# -------------------------
# Mathematische Operationen
# -------------------------

print("\nMathematische Operationen")
# Addition/Subtraktion/Mal/Division mit Skalar
# Jede dieser Operationen wird auf jedes Element des Arrays angewendet.
print("Addition von 1 zu jedem Element:\n", np.add(b, 1))
print("Subtraktion von 1 von jedem Element:\n", np.subtract(b, 1))
print("Multiplikation jedes Elements mit 2:\n", np.multiply(b, 2))
print("Division jedes Elements durch 2:\n", np.divide(b, 2))

# Potenzieren und Quadratwurzel
# Jedes Element wird quadriert (zum Quadrat erhoben) oder die Quadratwurzel wird gezogen.
print("Jedes Element wird quadriert:\n", np.power(b, 2))
print("Quadratwurzel jedes Elements:\n", np.sqrt(b))

# -------------------------
# Statistische Funktionen
# -------------------------

print("\nStatistische Funktionen")
# Diese Funktionen berechnen statistische Werte über das ganze Array.
print("Mittelwert (Durchschnitt):", np.mean(b))  # Mittelwert aller Elemente
print("Median:", np.median(b))  # Median ist der mittlere Wert, wenn alle Werte sortiert sind.
print("Standardabweichung:", np.std(b))  # Maß für die Verteilung der Werte
print("Varianz:", np.var(b))  # Quadrat der Standardabweichung
print("Minimum:", np.min(b))  # Der kleinste Wert im Array
print("Maximum:", np.max(b))  # Der größte Wert im Array

# -------------------------
# Array-Operationen und Manipulationen
# -------------------------

print("\nArray-Operationen und Manipulationen")
# Indexierung und Slicing
# Indexierung erlaubt den Zugriff auf bestimmte Elemente im Array.
print("Element an Position [0,1]:", b[0, 1])  # Zugriff auf das Element in Zeile 0, Spalte 1
print("Alle Elemente in Spalte 1:", b[:, 1])  # Zugriff auf alle Elemente in der 2. Spalte
print("Alle Elemente in Zeile 1:", b[1, :])  # Zugriff auf alle Elemente in der 2. Zeile

# Kombinieren und Teilen von Arrays
print("\nKombinieren und Teilen")
# Arrays können entlang verschiedener Achsen kombiniert werden.
print("Zusammenführen entlang der Zeilen (axis=0):\n", np.concatenate((b, b), axis=0))
print("Horizontaler Stack (nebeneinander):\n", np.hstack((b, b)))  # Horizontal nebeneinander
print("Vertikaler Stack (übereinander):\n", np.vstack((b, b)))  # Vertikal übereinander

# Teilen eines Arrays in kleinere Arrays
# "split" teilt das Array in die angegebene Anzahl von Teilen.
print("Teilen in 2 Teile:\n", np.split(b, 2))

# -------------------------
# Broadcasting
# -------------------------

print("\nBroadcasting")
# Broadcasting ist eine Methode, um Operationen auf Arrays unterschiedlicher Größe anzuwenden.
i = np.array([1, 2])
print("Array (1x2):\n", i)
# Hier wird das Array [1, 2] mit jeder Zeile der Matrix addiert.
print("Broadcasting Addition:\n", b + i)

# -------------------------
# Algebraische Operationen
# -------------------------

print("\nAlgebraische Operationen")
# Matrixmultiplikation
# Matrixmultiplikation (Dot-Produkt) multipliziert Zeilen mit Spalten und summiert die Ergebnisse.
print("Matrixmultiplikation:\n", np.dot(b, b))

# Inverse der Matrix
# Die Inverse einer Matrix ist eine Matrix, die mit der Originalmatrix multipliziert die Identitätsmatrix ergibt.
# Hinweis: Die Inverse existiert nur für quadratische Matrizen, die nicht singulär sind (Determinante ≠ 0).
print("Inverse der Matrix:\n", np.linalg.inv(b))

# Eigenwerte und Eigenvektoren
# Eigenwerte sind Skalare, die angeben, wie stark ein Eigenvektor bei der Transformation gestreckt wird.
# Eigenvektoren sind Vektoren, deren Richtung sich durch die Matrixtransformation nicht ändert.
print("Eigenwerte und Eigenvektoren:\n", np.linalg.eig(b))

# Lösen von Gleichungssystemen
# Löst das lineare Gleichungssystem Ax = b für x.
j = np.array([5, 6])
print("Lösen von Gleichungssystemen Ax=b:", np.linalg.solve(b, j))

# -------------------------
# Wahrheitswerte und Bedingungen
# -------------------------

print("\nWahrheitswerte und Bedingungen")
# Bedingte Operationen
# Überprüft jedes Element und gibt einen Wert basierend auf der Bedingung zurück.
print("Bedingung (Element > 2):", np.where(b > 2, 'Yes', 'No'))

# Überprüfen, ob alle Elemente eine Bedingung erfüllen
print("Alle Elemente > 0:", np.all(b > 0))

# Überprüfen, ob irgendein Element eine Bedingung erfüllt
print("Mindestens ein Element > 0:", np.any(b > 0))

# -------------------------
# Zufallszahlen
# -------------------------

print("\nZufallszahlen")
# Zufällige Werte zwischen 0 und 1
print("Zufällige Werte zwischen 0 und 1:\n", np.random.rand(2, 3))

# Zufällige Ganzzahlen zwischen zwei Werten
print("Zufällige Ganzzahlen zwischen 0 und 10:\n", np.random.randint(0, 10, size=(2, 3)))

# Seed für Reproduzierbarkeit
# Mit einem Seed kannst du sicherstellen, dass dieselben Zufallszahlen jedes Mal generiert werden.
np.random.seed(42)
print("Reproduzierbare Zufallszahlen:\n", np.random.rand(2, 3))

# -------------------------
# Fourier-Transformationen
# -------------------------

print("\nFourier-Transformationen")
# Fourier-Transformation
# Wandelt ein Signal in seine Frequenzkomponenten um.
print("Fourier-Transformation:\n", np.fft.fft(b))

# Inverse Fourier-Transformation
# Wandelt die Frequenzkomponenten zurück in das ursprüngliche Signal.
print("Inverse Fourier-Transformation:\n", np.fft.ifft(np.fft.fft(b)))
