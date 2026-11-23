from testData import load_csv_data
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

X, y, le = load_csv_data()
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "SGD": make_pipeline(StandardScaler(), SGDClassifier(random_state=42)),
    "SVC": make_pipeline(StandardScaler(), SVC()),
    "RandomForest": RandomForestClassifier(random_state=42)
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=cv)
    print(f"{name}: {scores.mean():.3f} +- {scores.std():.3f}")

y_pred = cross_val_predict(models["SVC"], X, y, cv=cv) #Error analysis on the SVC, using out-of-fold prediction

print(classification_report(y, y_pred, target_names=le.classes_))

ConfusionMatrixDisplay.from_predictions(
    y, y_pred, display_labels=le.classes_,
    normalize="true", sample_weight=(y_pred != y),
    values_format=".0%", cmap="Reds")
plt.show()