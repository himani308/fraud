import pandas as pd
import numpy as np

from flask import Flask, render_template

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Tools
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

# # Visualization
# import plotly.express as px

# import joblib

# app = Flask(__name__)


df = pd.read_csv("fraud_dataset_updated.csv")

# print("Dataset Shape:", df.shape)

# Clean data
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# Remove categorical columns
for col in df.columns:
    if df[col].dtype == 'object':
        print("Dropping column:", col)
        df.drop(col, axis=1, inplace=True)

# # Features & target
X = df.drop("Is_Fraud", axis=1)
y = df["Is_Fraud"]

# # Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# # Scaling logistiis regressssion
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


models = {
    "Logistic Regression": LogisticRegression(max_iter=3000),
    "Decision Tree": DecisionTreeClassifier(max_depth=8),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight='balanced'),
    "XGBoost": XGBClassifier(scale_pos_weight=10, eval_metric='logloss')
}

# results = []

# best_model = None
# best_score = 0
# best_name = ""

# for name, model in models.items():
#     print(f"\nTraining: {name}")

#     if name == "Logistic Regression":
#         model.fit(X_train_scaled, y_train)
#         y_pred = model.predict(X_test_scaled)
#         y_prob = model.predict_proba(X_test_scaled)[:, 1]
#         cv = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc').mean()
#     else:
#         model.fit(X_train, y_train)
#         y_pred = model.predict(X_test)
#         y_prob = model.predict_proba(X_test)[:, 1]
#         cv = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc').mean()

#     roc = roc_auc_score(y_test, y_prob)

#     print(classification_report(y_test, y_pred))
#     print("ROC-AUC:", roc)

#     results.append({
#         "Model": name,
#         "ROC_AUC": roc,
#         "CV_Score": cv
#     })

#     if roc > best_score:
#         best_score = roc
#         best_model = model
#         best_name = name

# print("\n BEST MODEL:", best_name)
# print("Best ROC-AUC:", best_score)

# # Save model
# joblib.dump(best_model, "best_model.pkl")
# joblib.dump(scaler, "scaler.pkl")

# results_df = pd.DataFrame(results)

# fig = px.bar(
#     results_df,
#     x="Model",
#     y="ROC_AUC",
#     color="Model",
#     text="ROC_AUC",
#     title="Model Comparison (ROC-AUC)"
# )

# fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
# fig.update_layout(
#     xaxis_title="Models",
#     yaxis_title="ROC-AUC Score"
# )

# graph_html = fig.to_html(full_html=False)


# @app.route("/")
# def home():
#     return render_template("comparison.html", graph=graph_html)
# if __name__ == "__main__":
#     app.run(debug=True)

from sklearn.metrics import accuracy_score, precision_score

results = []

for name, model in models.items():
    print(f"\nTraining: {name}")

    if name == "Logistic Regression":
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

    roc = roc_auc_score(y_test, y_prob)
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    results.append({
        "Model": name,
        "ROC_AUC": roc,
        "Accuracy": acc,
        "Precision": precision
    })
df_results = pd.DataFrame(results)
df_results.to_csv("model_results.csv", index=False)