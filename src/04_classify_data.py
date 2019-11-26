import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1 READING DATA

df_train = pd.read_csv('../output/df_train.csv')
df_pred = pd.read_csv('../output/df_pred.csv')

# Train data
X_train = df_train.loc[df_train.classification!='draw', ['score_nucleus','score_membrane']].reset_index(drop=True)
y_train = df_train.loc[df_train.classification!='draw', 'classification'].reset_index(drop=True)

# Random forest model
rf_model = RandomForestClassifier(n_estimators=11, random_state=42)

# Fit train data
rf_model.fit(np.array(X_train), list(y_train))

# Classify predicitons data
df_pred['preds'] = pd.DataFrame(rf_model.predict(df_pred[['score_nucleus','score_membrane']]))

# Save
df_pred.to_csv('../output/df_predictions.csv', index=False)