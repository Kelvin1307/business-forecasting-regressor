# Business Forecasting Regressor

Forecast TV, Radio, and Digital advertising budgets into sales revenue using a trained regression model.

## Project Structure

- `data/Advertising.csv` - Marketing dataset.
- `models/` - Saved model and scaler artifacts.
- `notebooks/exploration_modeling.ipynb` - EDA and modeling notebook.
- `backend/main.py` - FastAPI app and prediction endpoint.
- `backend/schemas.py` - Pydantic schema for input validation.
- `frontend/interface.py` - Streamlit dashboard.

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Train the model by running the notebook or the training script.

3. Start the API:

```bash
uvicorn backend.main:app --reload --port 8000
```

4. Run the frontend dashboard:

```bash
streamlit run frontend/interface.py
```

## API

POST `/predict/`

Request body:

```json
{
  "tv_budget": 250.0,
  "radio_budget": 50.0,
  "digital_budget": 120.0
}
```

Response:

```json
{
  "predicted_sales": 16.25
}
```
