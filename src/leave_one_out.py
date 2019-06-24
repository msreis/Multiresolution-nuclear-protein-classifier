def leave_one_out(data, model, response_var):
    import pandas as pd
    from sklearn.metrics import accuracy_score, precision_score, recall_score

    df_loo = pd.DataFrame(columns={'accuracy','precision','recall'})

    for i in range(0, data.shape[0]):

        X_train = data.loc[~data.index.isin([i]), data.columns != response_var]
        y_train = data.loc[~data.index.isin([i]), response_var]

        X_test = data.loc[i, data.columns != response_var]
        y_test = data.loc[i, response_var]

        # Train
        model.fit(X_train, y_train)
        # Make predictions
        y_pred = rf_model.predict(X_train)

        df_loo.loc[i, 'accuracy'] = accuracy_score(y_test, y_pred)
        df_loo.loc[i, 'precision'] = precision(y_test, y_pred)
        df_loo.loc[i, 'recall'] = recall(y_test, y_pred)

    return(df_loo)
