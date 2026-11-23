from testData import load_csv_data
from sklearn.preprocessing import StandardScaler
import numpy as np
import keras
from sklearn.model_selection import StratifiedKFold

X, y, le = load_csv_data()

def build_model(n_features, n_classes):
    model = keras.Sequential([
        keras.layers.Input(shape=(n_features,)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(n_classes, activation="softmax"),
    ])
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accs = []

for train_idx, val_idx in cv.split(X, y):
    scaler = StandardScaler().fit(X[train_idx]) #Fit on this fold's training part only
    X_tr = scaler.transform(X[train_idx])
    X_va = scaler.transform(X[val_idx])

    model = build_model(X.shape[1], len(le.classes_)) #Fresh model every fold
    model.fit(X_tr, y[train_idx], validation_data=(X_va, y[val_idx]),
              epochs=100, verbose=0,
              callbacks=[keras.callbacks.EarlyStopping(
                  patience=10, restore_best_weights=True)])
    accs.append(model.evaluate(X_va, y[val_idx], verbose=0)[1])

print(f"{np.mean(accs):.3f} +- {np.std(accs):.3f}")