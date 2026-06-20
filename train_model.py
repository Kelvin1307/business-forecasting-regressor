import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import os

DATA_PATH = os.path.join('data', 'Advertising.csv')
MODEL_DIR = 'models'


def load_data():
    df = pd.read_csv(DATA_PATH)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    return df


def train():
    df = load_data()
    df['Total_Budget'] = df[['TV', 'Radio', 'Newspaper']].sum(axis=1)
    df['TV_pct'] = df['TV'] / df['Total_Budget']
    df['Radio_pct'] = df['Radio'] / df['Total_Budget']
    df['Digital_pct'] = df['Newspaper'] / df['Total_Budget']

    features = ['TV', 'Radio', 'Newspaper']
    X = df[features]
    y = df['Sales']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    print('Linear Regression R2: %.4f' % r2_score(y_test, y_pred_lr))
    print('Linear Regression MAE: %.4f' % mean_absolute_error(y_test, y_pred_lr))

    rf = RandomForestRegressor(random_state=42)
    rf_param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [None, 6, 10],
        'min_samples_split': [2, 4],
    }
    rf_grid = GridSearchCV(rf, rf_param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
    rf_grid.fit(X_train_scaled, y_train)
    best_rf = rf_grid.best_estimator_
    y_pred_rf = best_rf.predict(X_test_scaled)
    rf_mae = mean_absolute_error(y_test, y_pred_rf)
    print('Random Forest R2: %.4f' % r2_score(y_test, y_pred_rf))
    print('Random Forest MAE: %.4f' % rf_mae)
    print('Best Random Forest params:', rf_grid.best_params_)

    xgb = XGBRegressor(random_state=42, objective='reg:squarederror', eval_metric='mae')
    xgb_param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.05, 0.1],
    }
    xgb_grid = GridSearchCV(xgb, xgb_param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
    xgb_grid.fit(X_train_scaled, y_train)
    best_xgb = xgb_grid.best_estimator_
    y_pred_xgb = best_xgb.predict(X_test_scaled)
    xgb_mae = mean_absolute_error(y_test, y_pred_xgb)
    print('XGBoost R2: %.4f' % r2_score(y_test, y_pred_xgb))
    print('XGBoost MAE: %.4f' % xgb_mae)
    print('Best XGBoost params:', xgb_grid.best_params_)

    if xgb_mae < rf_mae:
        best_model = best_xgb
        print('Selected model: XGBoost')
    else:
        best_model = best_rf
        print('Selected model: Random Forest')

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, os.path.join(MODEL_DIR, 'regression_model.pkl'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))
    print('Saved model and scaler to models/')


if __name__ == '__main__':
    train()
