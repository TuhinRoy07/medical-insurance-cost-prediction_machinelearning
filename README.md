<div align="center">

# 🏥 Medical Insurance Cost Prediction

### Predict yearly medical insurance charges with a tuned Random Forest model and an interactive Streamlit web app

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-compared-0B7A75)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

</div>

---

## 📌 Overview

This project predicts the **yearly medical insurance charges** of a person from six simple details: age, sex, BMI, number of children, smoking status and region.

It covers the complete machine learning workflow, from exploring the data to deploying the final model as a web app:

**EDA → Preprocessing → Baseline model → Model comparison (cross-validation) → Hyperparameter tuning → Final evaluation → Streamlit app**

## ✨ Features

- 📊 **Full EDA** with distributions, outlier checks, correlation heatmap and pairplot
- 🧪 **6 models compared** using 5-fold cross-validation
- 🎯 **Hyperparameter tuning** with `GridSearchCV` (576 combinations x 5 folds)
- 🧮 **Log-transformed target** to handle the skewed charges distribution
- 🔮 **Interactive web app** with a Predict button
- 🌙 **Light and Dark mode** switch
- 📈 **Charts** for smoking impact and cost by age
- 🧾 **Insights cards**: BMI category, comparison with dataset average, smoker vs non-smoker cost

## 📸 Screenshots

| Light mode | Dark mode |
|:---:|:---:|
| ![Light mode](screenshots/app-light.png) | ![Dark mode](screenshots/app-dark.png) |

## 📂 Dataset

- **Source:** [Medical Cost Personal Datasets (Kaggle)](https://www.kaggle.com/datasets/mirichoi0218/insurance/data)
- **Size:** 1,338 rows, 7 columns (1 duplicate row removed)

| Column | Description | Type |
|---|---|---|
| `age` | Age of the person | Numerical |
| `sex` | male / female | Categorical |
| `bmi` | Body Mass Index | Numerical |
| `children` | Number of dependents covered | Numerical |
| `smoker` | yes / no | Categorical |
| `region` | northeast, northwest, southeast, southwest | Categorical |
| `charges` | Yearly medical insurance cost (**target**) | Numerical |

## 🔍 Key Insights

- Charges are **highly right-skewed** with a few very expensive cases.
- **Smoking is the strongest factor.** Smokers pay several times more on average.
- Age and BMI have a moderate positive relationship with charges.
- There is no serious multicollinearity between the numeric features.

## 🧠 Methodology

| Step | What was done |
|---|---|
| Preprocessing | `StandardScaler` for numeric columns, `OneHotEncoder` for categorical columns, inside a `ColumnTransformer` + `Pipeline` (no data leakage) |
| Split | 80% train / 20% test, `random_state=42` |
| Baseline | Linear Regression |
| Models compared | Linear, Ridge, Lasso, Decision Tree, Random Forest, XGBoost (5-fold CV, MAE as primary metric) |
| Best model | **Random Forest** |
| Tuning | `GridSearchCV` on `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features` |
| Final model | Random Forest + `log1p` target transform (`TransformedTargetRegressor`) |

## 📊 Results

Cross-validation comparison (lower MAE is better):

| Model | CV MAE | CV R² |
|---|---:|---:|
| **Random Forest** | **~2,747** | **~0.82** |
| XGBoost | ~3,121 | ~0.78 |
| Decision Tree | ~3,284 | ~0.66 |
| Linear Regression | ~4,222 | ~0.72 |
| Lasso | ~4,222 | ~0.72 |
| Ridge | ~4,227 | ~0.72 |

Final tuned model on the held-out test set: **R² ≈ 0.90** and **MAE ≈ $2,000**.

> Exact numbers can differ slightly between machines because Random Forest uses randomness.

## 🗂️ Project Structure

```
medical-insurance-cost-prediction/
├── 15_5_medical_insurance_cost_pred.ipynb   # Full ML workflow
├── insurance.csv                            # Dataset
├── insurance_model.joblib                   # Trained model used by the app
├── app.py                                   # Streamlit web app
├── requirements.txt                         # Python dependencies
├── screenshots/                             # App screenshots for this README
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/medical-insurance-cost-prediction.git
cd medical-insurance-cost-prediction
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### 5. (Optional) Re-train the model

Open the notebook in VS Code or Jupyter, select the `venv` kernel and run all cells. The last cell saves a fresh `insurance_model.joblib`.

> ⏱️ The `GridSearchCV` cell tests 2,880 model fits and can take 5 to 10 minutes.

## 🖥️ How to Use the App

1. Choose the customer details in the sidebar (age, sex, BMI, children, smoker, region).
2. Click **🔮 Predict**.
3. View the estimated yearly and monthly cost, the comparison cards and the charts.
4. Use the **🌙 Dark mode** switch at the top of the sidebar to change the theme.

## 🛠️ Tech Stack

- **Language:** Python
- **Data and ML:** pandas, NumPy, scikit-learn, XGBoost
- **Visualization:** Matplotlib, Seaborn, Altair
- **Web app:** Streamlit
- **Tools:** Jupyter Notebook, VS Code, Git and GitHub

## 🔮 Future Improvements

- Deploy the app on Streamlit Community Cloud
- Add feature-importance and SHAP explanations
- Try more models and larger hyperparameter searches
- Add prediction history and downloadable reports

## ⚠️ Disclaimer

This project is for **learning and portfolio purposes only**. The predictions are estimates based on a public US dataset and are **not real insurance quotes**.

## 👤 Author

**Tuhin Roy**
Final-year BCA student | Data Analytics, SQL and AI/ML

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://www.linkedin.com/in/your-linkedin)

---

<div align="center">

⭐ If you found this project useful, please give it a star!

</div>
