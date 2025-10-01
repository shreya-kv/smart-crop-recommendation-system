# smart-crop-recommendation-system

# Overview

* This project is a machine learning–based smart crop system that recommends the top 3 most suitable crops based on soil parameters and   real-time weather conditions.
* Internally calculates profit and finalizes the most profitable crop.
* Recommends an irrigation method (Drip, Sprinkler, Subsurface Drip, Conventional) for each of the top 3 crops.
* Uses real-time weather API integration(not manual testing) for more accurate recommendations.

# Motivation

Farmers often struggle to decide which crop will give them the best yield and profit under uncertain weather conditions. This system provides data-driven crop recommendations, ensuring better productivity, profitability, and efficient resource usage.

# Features

* Fetches real-time weather data(temperature, rainfall, humidity, etc.) using API integration.
* Uses a machine learning model(Random Forest) trained on agricultural datasets.
* Recommends the most profitable crop after evaluating cost, yield, and market prices.
* Suggests irrigation methods for sustainable water usage.
* Deployed as a web app for easy access and use.

# Tech Stack

* Languages: Python
* Frameworks/Tools: Flask
* Libraries: pandas, joblib, scikit-learn, requests (for API)
* APIs: OpenWeatherMap API
* Version Control: Git & GitHub

# Dataset

1)Crop dataset
  * Crop
  * Season
  * N category
  * P category
  * K category
  * Water requirement
  * Root depth
  * Soil type
  * Temperature
  * Temperature range
  * Humidity
  * Humidity range
  * Rainfall
  * Rainfall range
  * PH
  * PH range
    
2) Profit dataset
  * Cost of Cultivation
  * Yield per Hectare
  * Market Price (MSP)
  * Revenue & Profit
  
# How It Works

1. User provides soil parameters.
2. System fetches real-time weather data from API.
3. ML model predicts top 3 crops.
4. Profit is calculated internally → system picks the most profitable crop.
5. Displays irrigation suggestions for all top 3 crops along with the predicted 3 crops and the calculated most profitable crop on the     web app.

# Results

* Mean CV Accuracy: 0.9982300884955752
* Real-time weather integration improved recommendation reliability.


---

👉 Do you want me to make this **ready-to-paste READM
