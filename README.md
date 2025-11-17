# 🚗 Dynamic Pricing System for Ride-Sharing

A machine learning project that predicts ride demand to find the revenue-maximizing price. The final model is served via a **FastAPI** and made interactive with a **Streamlit** dashboard.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Data Science:** Pandas, Scikit-learn, Joblib
* **API:** FastAPI, Uvicorn
* **Dashboard:** Streamlit

---

## 🏃 How to Run

### 1. Prerequisites

* Install libraries: `pip install pandas scikit-learn joblib fastapi uvicorn streamlit requests`
* Have the `ride_sharing_data.csv` file in the root folder.

### 2. Train the Model

Run this once to create the `demand_model_v1.joblib` file.
```powershell
python src/train.py
