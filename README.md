
# 🏡 Real Estate Price Prediction – Saudi Arabia

This project is a **machine learning solution** designed to predict real estate prices across **Saudi Arabia** using **real open data** provided by the **Saudi Open Data Platform**. It aims to empower investors, clients, and researchers with **accurate and data-driven property price estimates**.

---

## 📊 Project Overview

The model uses **real Saudi property transaction data**, including:

* Region, city, and district
* Property type and classification
* Area 
* Actual sale prices

**Goal:** Provide a reliable tool to estimate property prices based on location and property characteristics.

**Impact:**

* Supports **decision-making** in the real estate market
* Helps buyers and investors **assess property values** accurately
* Delivers **realistic predictions** using trustworthy data

---


## 🗂️ About the Data

* **Source:** Saudi Open Data Platform
* **Type:** Real property sales transactions
* **Content:** Detailed property information including location, type, area, units, and price
* **Benefit:** Provides a realistic representation of the **Saudi real estate market** to enable accurate predictions



## 📅 Dataset Details

The dataset used in this project consists of real estate sales transactions from different quarters of the same year:

Q2 dataset → used for training the machine learning model

Q3 dataset → used for final evaluation and testing

This separation ensures fair performance assessment and prevents data leakage, providing a realistic evaluation of how the model performs on unseen data. 

---



## ⚙️ Technologies Used

* **Python** for scripting and data processing
* **Pandas & NumPy** for data manipulation
* **Scikit-learn** for machine learning models (Random Forest Regressor)
* **Joblib** for saving and loading models and preprocessors
* **RobustScaler** for handling outliers in numerical features
* **LabelEncoder** for transforming categorical features
* **Azure ML** for model registration and deployment
* **Azure Container Instances (ACI)** for hosting the model
* **Gradio** for interactive web interface

---

## 🏆 Key Features

* **Handles numerical and categorical features** efficiently
* **Preprocessing pipeline** ensures consistency between training and inference
* **Robust scaling** reduces the impact of extreme values in property area
* **Random Forest Regressor** delivers accurate price predictions
* **Supports real-time predictions** via Azure ML deployment
* **Interactive Gradio interface** for user-friendly input and output

---

## 🔒 Security & Best Practices

* Do **not commit sensitive files** such as `config.json` (Azure credentials) in public repositories
* Gradio public URLs are temporary and expire when the session ends


---


`Data → Preprocessing → Model → Azure ML → Gradio`  

