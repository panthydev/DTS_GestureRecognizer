#import joblib
#
#final = make_pipeline(StandardScaler(), SVC()).fit(X, y)
#joblib.dump(final, "model.joblib")
#joblib.dump(le, "label_encoder.joblib")