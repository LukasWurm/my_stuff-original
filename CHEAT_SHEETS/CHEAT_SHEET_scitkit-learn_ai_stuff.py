"""
Scikit-learn Library Cheat Sheet
=================================
This script demonstrates the basic usage of the Scikit-learn library in Python, 
which is used for machine learning tasks like data preprocessing, model training, and evaluation.
"""

from sklearn.datasets import load_iris  # Importing a sample dataset
from sklearn.model_selection import train_test_split  # Function to split data into training and testing sets
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.neighbors import KNeighborsClassifier  # KNN classifier
from sklearn.metrics import accuracy_score  # Function to calculate accuracy

# -------------------------
# Loading and Exploring Data
# -------------------------

# Loading the Iris dataset
data = load_iris()
X, y = data.data, data.target  # Features and labels

# -------------------------
# Splitting Data
# -------------------------

# Splitting the dataset into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------
# Feature Scaling
# -------------------------

# Initializing the StandardScaler
scaler = StandardScaler()

# Fitting and transforming the training data
X_train_scaled = scaler.fit_transform(X_train)

# Transforming the testing data (using the same scaler fit on training data)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# Training a KNN Classifier
# -------------------------

# Initializing the KNN classifier with 3 neighbors
knn = KNeighborsClassifier(n_neighbors=3)

# Training the model
knn.fit(X_train_scaled, y_train)

# -------------------------
# Making Predictions and Evaluating
# -------------------------

# Predicting the labels for the test set
y_pred = knn.predict(X_test_scaled)

# Calculating accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')  # Prints the accuracy of the model
