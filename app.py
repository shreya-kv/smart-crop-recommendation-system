# from flask import Flask, request, render_template
# import joblib
# import pandas as pd
# import os
# import csv
# import requests

# app = Flask(__name__)

# # Project base directory (safe path handling)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Load ML model and profit data
# MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")
# PROFIT_PATH = os.path.join(BASE_DIR, "profit_data.csv")
# model = joblib.load(MODEL_PATH)
# profit_df = pd.read_csv(PROFIT_PATH, encoding="utf-8")

# # OpenWeatherMap API key (use env variable for safety)
# API_KEY = os.environ.get("OPENWEATHER_API_KEY", "your_api_key_here")

# # Crop translation (English → Hindi)
# translations = {
#     'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का',
#     'pigeonpeas': 'अरहर', 'chickpea': 'चना', 'mungbean': 'मूंग',
#     'mothbeans': 'मटकी', 'blackgram': 'उड़द', 'lentil': 'मसूर',
#     'pomegranate': 'अनार', 'banana': 'केला', 'mango': 'आम',
#     'grapes': 'अंगूर', 'apple': 'सेब', 'muskmelon': 'खरबूजा',
#     'watermelon': 'तरबूज', 'orange': 'संतरा', 'papaya': 'पपीता',
#     'coconut': 'नारियल', 'cotton': 'कपास', 'jute': 'जूट',
#     'coffee': 'कॉफी'
# }

# # Crop categories for rotation logic
# crop_categories = {
#     'rice': 'cereal', 'wheat': 'cereal', 'maize': 'cereal',
#     'pigeonpeas': 'legume', 'chickpea': 'legume', 'mungbean': 'legume',
#     'mothbeans': 'legume', 'blackgram': 'legume', 'lentil': 'legume',
#     'banana': 'fruit', 'mango': 'fruit', 'grapes': 'fruit',
#     'apple': 'fruit', 'muskmelon': 'fruit', 'watermelon': 'fruit',
#     'papaya': 'fruit', 'orange': 'fruit', 'pomegranate': 'fruit',
#     'coconut': 'fruit', 'cotton': 'fiber', 'jute': 'fiber',
#     'coffee': 'cash'
# }

# # Micro-irrigation suggestions
# micro_irrigation_crops = {
#     'apple': 'Recommended: Drip irrigation for precise water control in orchards.',
#     'banana': 'Highly recommended: Drip irrigation increases productivity and saves water.',
#     'blackgram': 'Sprinkler or furrow irrigation can be used; micro-irrigation is optional.',
#     'chickpea': 'Low water crop, drip irrigation can be used during flowering for efficiency.',
#     'coconut': 'Drip irrigation ensures deep root watering and improves yield.',
#     'coffee': 'Drip preferred in plantations to optimize water usage.',
#     'cotton': 'Highly efficient with drip irrigation for uniform flowering and boll formation.',
#     'grapes': 'Drip irrigation is ideal for controlled water delivery and quality improvement.',
#     'jute': 'Generally rainfed; micro-irrigation is not widely practiced.',
#     'kidneybeans': 'Can use sprinkler; drip optional but helps in drought conditions.',
#     'lentil': 'Moderate water crop; drip irrigation improves water efficiency.',
#     'maize': 'Sprinkler preferred; drip is effective in low rainfall areas.',
#     'mango': 'Drip irrigation helps increase fruit size and yield in orchards.',
#     'mothbeans': 'Rainfed; minimal irrigation needed. Micro-irrigation optional.',
#     'mungbean': 'Can use sprinkler or drip during dry spells for better yield.',
#     'muskmelon': 'Drip irrigation is preferred for consistent soil moisture.',
#     'orange': 'Drip irrigation helps manage soil salinity and improves fruit quality.',
#     'papaya': 'Drip preferred due to shallow root system and frequent watering need.',
#     'pigeonpeas': 'Moderate irrigation needed; drip helps during flowering stage.',
#     'pomegranate': 'Highly recommended: Drip irrigation ensures better fruit size and saves water.',
#     'rice': 'Traditionally flood-irrigated, but alternate wetting and drying or drip is emerging.',
#     'watermelon': 'Drip irrigation ensures uniform moisture and reduces fruit cracking.'
# }

# @app.route('/')
# def index():
#     return render_template("index.html")

# # Feedback route
# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         name = request.form.get('name', '')
#         email = request.form.get('email', '')
#         message = request.form.get('message', '')

#         file = os.path.join(BASE_DIR, 'feedback.csv')
#         file_exists = os.path.isfile(file)
#         with open(file, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(['Name', 'Email', 'Message'])
#             writer.writerow([name, email, message])

#         return render_template('thankyou.html')
#     return render_template('feedback.html')

# # Farmer request form page
# @app.route('/farmer', methods=['GET', 'POST'])
# def farmer():
#     if request.method == 'POST':
#         name = request.form['name']
#         location = request.form['location']

#         file = os.path.join(BASE_DIR, 'farmer_requests.csv')
#         file_exists = os.path.isfile(file)
#         with open(file, 'a', newline='', encoding="utf-8") as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(['name', 'location'])
#             writer.writerow([name, location])

#         return render_template("check_result.html", name=name, location=location)

#     return render_template("farmer.html")

# # Result page (fetch linked tester data)
# @app.route('/result', methods=['POST'])
# def result():
#     name = request.form['name']
#     location = request.form['location']

#     tester_file = os.path.join(BASE_DIR, "linked_tester_data.csv")
#     if not os.path.exists(tester_file):
#         return "Tester data not found. Please wait for soil report."

#     df = pd.read_csv(tester_file, encoding="utf-8")
#     matched = df[(df['name'] == name) & (df['location'] == location)]
#     if matched.empty:
#         return "Tester has not yet submitted data for this farmer."

#     tester_data = matched.iloc[-1]
#     input_data = [[tester_data['N'], tester_data['P'], tester_data['K'],
#                    tester_data['temperature'], tester_data['humidity'],
#                    tester_data['ph'], tester_data['rainfall']]]
#     crop = model.predict(input_data)[0]

#     translated_crop = translations.get(crop, crop)
#     irrigation = micro_irrigation_crops.get(crop, "Standard irrigation method is sufficient.")

#     # Profit lookup
#     row = profit_df[profit_df['crop'] == crop]
#     profit = int(row['estimated_profit'].values[0]) if not row.empty else "N/A"

#     return render_template("result.html", crop=crop, translated_crop=translated_crop,
#                            profit=profit, irrigation=irrigation)

# # Tester route
# @app.route('/tester', methods=['GET', 'POST'])
# def tester():
#     if request.method == 'POST':
#         try:
#             name = request.form['name']
#             location = request.form['location']
#             N = float(request.form['N'])
#             P = float(request.form['P'])
#             K = float(request.form['K'])
#             temperature = float(request.form['temperature'])
#             humidity = float(request.form['humidity'])
#             ph = float(request.form['ph'])
#             rainfall = float(request.form['rainfall'])
#             soil_type = request.form.get('soil_type')
#             season = request.form.get('season')
#             water_level = request.form.get('water_level')
#             fertilizer_required = request.form.get('fertilizer_required')
#             pest_present = request.form.get('pest_present')

#             input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
#             crop = model.predict(input_data)[0]
#             translated_crop = translations.get(crop, crop)
#             irrigation = micro_irrigation_crops.get(crop, "Standard irrigation method is sufficient.")

#             row = profit_df[profit_df['crop'] == crop]
#             profit = int(row['estimated_profit'].values[0]) if not row.empty else "N/A"

#             # Save tester data (always ensures farmer-result linking works)
#             file = os.path.join(BASE_DIR, 'linked_tester_data.csv')
#             file_exists = os.path.isfile(file)
#             with open(file, 'a', newline='', encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 if not file_exists:
#                     writer.writerow(['name', 'location', 'N', 'P', 'K', 'temperature', 'humidity',
#                                      'ph', 'rainfall', 'crop', 'soil_type', 'season',
#                                      'water_level', 'fertilizer_required', 'pest_present'])
#                 writer.writerow([name, location, N, P, K, temperature, humidity, ph, rainfall,
#                                  crop, soil_type, season, water_level, fertilizer_required, pest_present])

#             return render_template("result.html", crop=crop, translated_crop=translated_crop,
#                                    profit=profit, irrigation=irrigation)
#         except Exception as e:
#             return f"Error: {str(e)}"
#     return render_template("tester.html")

# #WEATHER API

# @app.route("/predict", methods=["POST"])
# def predict():
#     location = request.form["location"]
#     api_key = "eba7a9462af4cfa2bd8c3de9fbd5e887"

#     # Call OpenWeatherMap API
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
#     response = requests.get(url).json()

#     if response.get("main"):
#         temperature = response["main"]["temp"]
#         humidity = response["main"]["humidity"]
#         rainfall = response.get("rain", {}).get("1h", 0)  # Rain in last 1 hour (if available)
#     else:
#         temperature = 25
#         humidity = 60
#         rainfall = 0

#     # Now pass these values into your ML model along with soil data
#     prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

#     return render_template(
#         "result.html",
#         crop=prediction[0],
#         profit=45000,
#         irrigation="Use drip irrigation",
#         used_tester_data=False
#     )

# # LANGUAGE OPTIONS
#     from googletrans import Translator

#     translator = Translator()

#     @app.route("/predict", methods=["POST"])
#     def predict():
#         language = request.form["language"]
#         crop = "Rice"

#         # Translate crop name if not English
#         translated_crop = translator.translate(crop, dest=language).text

#         return render_template(
#             "result.html",
#             crop=crop,
#             translated_crop=translated_crop,
#             profit=50000,
#             irrigation="Use drip irrigation",
#             used_tester_data=False
#         )

# if __name__ == '__main__':
#     app.run(debug=True)




















# from flask import Flask, request, render_template, redirect, url_for
# import joblib
# import pandas as pd
# import os
# import csv
# import requests
# from deep_translator import GoogleTranslator


# app = Flask(__name__)

# # ========== Paths & config ==========
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")
# PROFIT_PATH = os.path.join(BASE_DIR, "profit_data.csv")
# LINKED_TESTER_FILE = os.path.join(BASE_DIR, "linked_tester_data.csv")
# FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.csv")
# FARMER_REQUESTS_FILE = os.path.join(BASE_DIR, "farmer_requests.csv")

# # Load model and profit data
# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Place crop_model.pkl there.")

# model = joblib.load(MODEL_PATH)

# if os.path.exists(PROFIT_PATH):
#     profit_df = pd.read_csv(PROFIT_PATH, encoding="utf-8")
# else:
#     # create empty dataframe placeholder if not present
#     profit_df = pd.DataFrame(columns=["crop", "estimated_profit"])

# # Weather API key from env (recommended)
# OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", None)


# # Helpful dictionaries (you already had these; keep them)
# translations = {
#     # 'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का',
#     # 'pigeonpeas': 'अरहर', 'chickpea': 'चना', 'mungbean': 'मूंग',
#     # 'mothbeans': 'मटकी', 'blackgram': 'उड़द', 'lentil': 'मसूर',
#     # 'pomegranate': 'अनार', 'banana': 'केला', 'mango': 'आम',
#     # 'grapes': 'अंगूर', 'apple': 'सेब', 'muskmelon': 'खरबूजा',
#     # 'watermelon': 'तरबूज', 'orange': 'संतरा', 'papaya': 'पपीता',
#     # 'coconut': 'नारियल', 'cotton': 'कपास', 'jute': 'जूट',
#     # 'coffee': 'कॉफी'
    
#     'rice':        {'hi':'चावल', 'kn':'ಅಕ್ಕಿ', 'ta':'அரிசி', 'te':'అన్నం', 'bn':'চাউল', 'ml':'അരി', 'mr':'तांदूळ', 'gu':'ચોખા', 'pa':'ਚੌਲ'},
#     'wheat':       {'hi':'गेहूं', 'kn':'ಗೋಧಿ', 'ta':'கோதுமை', 'te':'గోధుమ', 'bn':'গম', 'ml':'ഗോതമ്പ്', 'mr':'गहू', 'gu':'ઘઉં', 'pa':'ਗੰਹੁ'},
#     'maize':       {'hi':'मक्का', 'kn':'ಜೋಳ', 'ta':'மக்காச்சோளம்', 'te':'మక్కజొన్న', 'bn':'ভুট্টা', 'ml':'മക്ക', 'mr':'मकई', 'gu':'મકાઈ', 'pa':'ਮੱਕਾ'},
#     'pigeonpeas':  {'hi':'अरहर', 'kn':'ತುರಿ ಬೇಳೆ', 'ta':'துவரம்பருப்பு', 'te':'తుర దాలు', 'bn':'আরহার', 'ml':'ടുവർപയർ', 'mr':'अरहर', 'gu':'તુવાર', 'pa':'ਤੂਵਰ'},
#     'chickpea':    {'hi':'चना', 'kn':'ಕಡಲೆ ಬೇಳೆ', 'ta':'கடலை பருப்பு', 'te':'చనగ', 'bn':'ছোলা', 'ml':'ചേനാപയർ', 'mr':'हरभरा', 'gu':'ચણો', 'pa':'ਛੋਲਾ'},
#     'mungbean':    {'hi':'मूंग', 'kn':'ಮุงಿ', 'ta':'பாசிப்பருப்பு', 'te':'మినుములు', 'bn':'মুগ', 'ml':'പച്ചപ്പയർ', 'mr':'मूग', 'gu':'મગ', 'pa':'ਮੂੰਗ'},
#     'mothbeans':   {'hi':'मटकी', 'kn':'ಮಟ್ಕಿ', 'ta':'மாத்பருப்பு', 'te':'మోత బీన్', 'bn':'মটকি', 'ml':'മട്ടക്കി', 'mr':'मतकी', 'gu':'મઠ', 'pa':'ਮਟਕੀ'},
#     'blackgram':   {'hi':'उड़द', 'kn':'ಉದ್ದಿನ ಬೇಳೆ', 'ta':'உளுந்து', 'te':'ఉద్దు', 'bn':'উড়দ', 'ml':'കടല', 'mr':'उडीद', 'gu':'ઉડદ', 'pa':'ਉਰਦ'},
#     'lentil':      {'hi':'मसूर', 'kn':'ಹಸಿರು ಕಡಲೆ', 'ta':'பருப்பு', 'te':'పసుపు దాల్', 'bn':'মসুর', 'ml':'പരിപ്പ്', 'mr':'मसूर', 'gu':'મસૂર', 'pa':'ਮਸੂਰ'},
#     'pomegranate': {'hi':'अनार', 'kn':'ದಾಳಿಂಬೆ', 'ta':'மாதுளை', 'te':'దానిమ్మ', 'bn':'ডালিম', 'ml':'മത്തളം', 'mr':'डाळिंब', 'gu':'ડાળિમ', 'pa':'ਅਨਾਰ'},
#     'banana':      {'hi':'केला', 'kn':'ಬಾಳೆಹಣ್ಣು', 'ta':'வாழைப்பழம்', 'te':'బనానా', 'bn':'কলা', 'ml':'പഴം', 'mr':'केळी', 'gu':'કેલો', 'pa':'ਕੇਲਾ'},
#     'mango':       {'hi':'आम', 'kn':'ಮಾವು', 'ta':'மாம்பழம்', 'te':'మామిడి', 'bn':'আম', 'ml':'മാങ്ങ', 'mr':'आंबा', 'gu':'કેરી', 'pa':'ਆਮ'},
#     'grapes':      {'hi':'अंगूर', 'kn':'ದ್ರಾಕ್ಷಿ', 'ta':'திராட்சை', 'te':'ద్రాక్ష', 'bn':'আঙুর', 'ml':'മുന്തിരി', 'mr':'द्राक्ष', 'gu':'દ્રાક્ષ', 'pa':'ਅੰਗੂਰ'},
#     'apple':       {'hi':'सेब', 'kn':'ಸೇಬು', 'ta':'ஆப்பிள்', 'te':'సేపు', 'bn':'আপেল', 'ml':'ആപ്പിൾ', 'mr':'सफरचंद', 'gu':'સફરજન', 'pa':'ਸੇਬ'},
#     'muskmelon':   {'hi':'खरबूजा', 'kn':'ಹನುಮಾಣಿ', 'ta':'செம்பருத்தி', 'te':'గంధపండు', 'bn':'খরবুজা', 'ml':'കപുത്ത്', 'mr':'खरबूज', 'gu':'ખરબુજ', 'pa':'ਖਰਬੂਜ'},
#     'watermelon':  {'hi':'तरबूज', 'kn':'ತರಬೂಜ', 'ta':'தர்பூசணி', 'te':'తర్బూజు', 'bn':'তরমুজ', 'ml':'തര്ബൂജം', 'mr':'कलिंगड', 'gu':'તર્બૂજ', 'pa':'ਤਰਬੂਜ'},
#     'orange':      {'hi':'संतरा', 'kn':'ಸಂತರ', 'ta':'ஆரஞ்சு', 'te':'నారింజ', 'bn':'কমলা', 'ml':'ഓറഞ്ച്', 'mr':'संत्रा', 'gu':'નારંગી', 'pa':'ਸੰਤਰਾ'},
#     'papaya':      {'hi':'पपीता', 'kn':'ಪಪಾಯಾ', 'ta':'பப்பாளி', 'te':'బొప్పాయి', 'bn':'পেঁপে', 'ml':'പപ്പായ', 'mr':'पपई', 'gu':'પપૈયા', 'pa':'ਪਪੀਤਾ'},
#     'coconut':     {'hi':'नारियल', 'kn':'ತೆಂಗಿನಕಾಯಿ', 'ta':'தேங்காய்', 'te':'కొబ్బరి', 'bn':'নারকেল', 'ml':'തേങ്ങ്', 'mr':'नारळ', 'gu':'નાળિયેર', 'pa':'ਨਾਰੀਅਲ'},
#     'cotton':      {'hi':'कपास', 'kn':'ಹತ್ತಿ', 'ta':'பருத்தி', 'te':'పత్తి', 'bn':'সুত', 'ml':'പല്ല്', 'mr':'कापूस', 'gu':'કપાસ', 'pa':'ਕਪਾਹ'},
#     'jute':        {'hi':'जूट', 'kn':'ಜ್ಯೂಟ್', 'ta':'ஜூட்', 'te':'జ్యూట్', 'bn':'জুট', 'ml':'ജ്യൂട്ട്', 'mr':'जूट', 'gu':'જુટ', 'pa':'ਜੂਟ'},
#     'coffee':      {'hi':'कॉफी', 'kn':'ಕಾಫಿ', 'ta':'காபி', 'te':'కాఫీ', 'bn':'কফি', 'ml':'കാപ്പി', 'mr':'कॉफी', 'gu':'કાફી', 'pa':'ਕੌਫੀ'}

# }

# micro_irrigation_crops = {
#     'apple': 'Recommended: Drip irrigation for precise water control in orchards.',
#     'banana': 'Highly recommended: Drip irrigation increases productivity and saves water.',
#     'blackgram': 'Sprinkler or furrow irrigation can be used; micro-irrigation is optional.',
#     'chickpea': 'Low water crop, drip irrigation can be used during flowering for efficiency.',
#     'coconut': 'Drip irrigation ensures deep root watering and improves yield.',
#     'coffee': 'Drip preferred in plantations to optimize water usage.',
#     'cotton': 'Highly efficient with drip irrigation for uniform flowering and boll formation.',
#     'grapes': 'Drip irrigation is ideal for controlled water delivery and quality improvement.',
#     'jute': 'Generally rainfed; micro-irrigation is not widely practiced.',
#     'lentil': 'Moderate water crop; drip irrigation improves water efficiency.',
#     'maize': 'Sprinkler preferred; drip is effective in low rainfall areas.',
#     'mango': 'Drip irrigation helps increase fruit size and yield in orchards.',
#     'mungbean': 'Can use sprinkler or drip during dry spells for better yield.',
#     'muskmelon': 'Drip irrigation is preferred for consistent soil moisture.',
#     'orange': 'Drip irrigation helps manage soil salinity and improves fruit quality.',
#     'papaya': 'Drip preferred due to shallow root system and frequent watering need.',
#     'pigeonpeas': 'Moderate irrigation needed; drip helps during flowering stage.',
#     'pomegranate': 'Highly recommended: Drip irrigation ensures better fruit size and saves water.',
#     'rice': 'Traditionally flood-irrigated; alternate wetting and drying or drip is emerging.',
#     'watermelon': 'Drip irrigation ensures uniform moisture and reduces fruit cracking.'
# }

# # ========== Utility helpers ==========
# def fetch_weather_for_location(location: str):
#     """Return (temperature_C, humidity_pct, rainfall_mm) — fallback defaults if API fails."""
#     default = (25.0, 60.0, 0.0)
#     if not OPENWEATHER_API_KEY:
#         return default
#     try:
#         url = (
#             f"http://api.openweathermap.org/data/2.5/weather"
#             f"?q={requests.utils.quote(location)}&appid={OPENWEATHER_API_KEY}&units=metric"
#         )
#         resp = requests.get(url, timeout=6)
#         resp.raise_for_status()
#         data = resp.json()
#         main = data.get("main", {})
#         temp = main.get("temp", default[0])
#         hum = main.get("humidity", default[1])
#         rain = data.get("rain", {})
#         # try hourly rain (1h) then (3h)
#         rainfall = rain.get("1h", rain.get("3h", 0.0))
#         return float(temp), float(hum), float(rainfall)
#     except Exception:
#         return default

# def lookup_profit_for_crop(crop_name: str):
#     if profit_df is None or profit_df.empty:
#         return "N/A"
#     row = profit_df[profit_df['crop'].astype(str).str.lower() == str(crop_name).lower()]
#     if not row.empty:
#         try:
#             return int(row['estimated_profit'].values[0])
#         except Exception:
#             return row['estimated_profit'].values[0]
#     return "N/A"

# def translate_crop_name(crop_name: str, dest_lang: str):
#     try:
#         if not dest_lang or dest_lang == "en":
#             return crop_name
#         return GoogleTranslator(source="en", target=dest_lang).translate(crop_name)
#     except Exception:
#         return crop_name

# def save_csv_row(filepath, header, row):
#     file_exists = os.path.isfile(filepath)
#     with open(filepath, 'a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(header)
#         writer.writerow(row)

# # ========== Routes ==========
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Farmer form: GET shows form, POST processes farmer submission (fetch weather, try linked tester, predict)
# @app.route('/farmer', methods=['GET', 'POST'])
# def farmer():
#     if request.method == 'POST':
#         # collect farmer inputs
#         name = request.form.get('name', '').strip()
#         location = request.form.get('location', '').strip()
#         phone = request.form.get('phone', '').strip()
#         language = request.form.get('language', 'en')

#         # save farmer request (log)
#         header = ['Name', 'Location', 'Phone', 'Language']
#         row = [name, location, phone, language]
#         save_csv_row(FARMER_REQUESTS_FILE, header, row)

#         # 1) Try to find linked tester data for the farmer
#         used_tester_data = False
#         last_crop = None
#         if os.path.exists(LINKED_TESTER_FILE):
#             try:
#                 df = pd.read_csv(LINKED_TESTER_FILE, encoding='utf-8')
#                 # match rows by name & location (case-insensitive)
#                 matched = df[(df['name'].astype(str).str.lower() == name.lower()) &
#                              (df['location'].astype(str).str.lower() == location.lower())]
#                 if not matched.empty:
#                     tester_data = matched.iloc[-1]  # latest
#                     input_data = [[
#                         float(tester_data.get('N', 80)),
#                         float(tester_data.get('P', 40)),
#                         float(tester_data.get('K', 40)),
#                         float(tester_data.get('temperature', 25)),
#                         float(tester_data.get('humidity', 60)),
#                         float(tester_data.get('ph', 6.5)),
#                         float(tester_data.get('rainfall', 0))
#                     ]]
#                     used_tester_data = True
#                     last_crop = str(tester_data.get('crop', ''))
#                 else:
#                     input_data = None
#             except Exception:
#                 input_data = None
#         else:
#             input_data = None

#         # 2) If no tester data, fetch weather and use default or estimated soil values
#         if input_data is None:
#             temp, hum, rain = fetch_weather_for_location(location)
#             # DEFAULT soil guesses (you may refine)
#             N, P, K, ph = 80.0, 40.0, 40.0, 6.5
#             input_data = [[N, P, K, temp, hum, ph, rain]]

#         # 3) ML prediction
#         try:
#             crop_pred = model.predict(input_data)[0]
#         except Exception as e:
#             return f"Model prediction failed: {e}"

#         # translate & suggestions
#         translated_crop = translate_crop_name(crop_pred, language)
#         irrigation = micro_irrigation_crops.get(crop_pred.lower(), "Standard irrigation method is sufficient.")
#         profit = lookup_profit_for_crop(crop_pred)

#         # Build a simple top_crops list (by highest profit) excluding main crop — frontend expects top_crops list
#         top_crops = []
#         try:
#             if not profit_df.empty:
#                 # take top 4 profitable crops and exclude predicted crop, then take top3
#                 tmp = profit_df.copy()
#                 tmp['crop_lower'] = tmp['crop'].astype(str).str.lower()
#                 tmp = tmp[tmp['crop_lower'] != str(crop_pred).lower()]
#                 tmp = tmp.sort_values(by='estimated_profit', ascending=False).head(3)
#                 top_crops = list(zip(tmp['crop'].astype(str).tolist(), tmp['estimated_profit'].astype(int).tolist()))
#         except Exception:
#             top_crops = []

#         return render_template(
#             "result.html",
#             crop=crop_pred,
#             translated_crop=translated_crop,
#             profit=profit,
#             irrigation=irrigation,
#             used_tester_data=used_tester_data,
#             last_crop=last_crop,
#             top_crops=top_crops
#         )

#     # GET request -> show form
#     return render_template("farmer.html")


# # Feedback route (improved: collects phone, rating etc if provided by frontend)
# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         name = request.form.get('name', '')
#         phone = request.form.get('phone', '')
#         email = request.form.get('email', '')
#         location = request.form.get('location', '')
#         experience = request.form.get('experience', '')
#         rating = request.form.get('rating', '')
#         recommend = request.form.get('recommend', '')
#         message = request.form.get('message', '')

#         header = ['Name', 'Phone', 'Email', 'Location', 'Experience', 'Rating', 'Recommend', 'Message']
#         row = [name, phone, email, location, experience, rating, recommend, message]
#         save_csv_row(FEEDBACK_FILE, header, row)

#     return render_template('feedback.html')

# @app.route('/feedback_submit')
# def feedback_submit():
#     return render_template('feedback_submit.html')


# # Tester route: show tester.html (GET) and accept soil data (POST)
# @app.route('/tester', methods=['GET', 'POST'])
# def tester():
#     if request.method == 'POST':
#         try:
#             name = request.form.get('name', '').strip()
#             phone = request.form.get('phone', '').strip()
#             location = request.form.get('location', '').strip()
#             N = float(request.form.get('N', 0))
#             P = float(request.form.get('P', 0))
#             K = float(request.form.get('K', 0))
#             temperature = float(request.form.get('temperature', 25))
#             humidity = float(request.form.get('humidity', 60))
#             ph = float(request.form.get('ph', 6.5))
#             rainfall = float(request.form.get('rainfall', 0))
#             soil_type = request.form.get('soil_type', '')
#             season = request.form.get('season', '')
#             water_level = request.form.get('water_level', '')
#             # match frontend field names (choose whichever you used)
#             fertilizer_required = request.form.get('fertilizer') or request.form.get('fertilizer_required') or ''
#             pest_present = request.form.get('pest') or request.form.get('pest_present') or ''

#             # Predict using tester data
#             input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
#             crop_pred = model.predict(input_data)[0]
#             translated_crop = translate_crop_name(crop_pred, 'en')  # default english here
#             irrigation = micro_irrigation_crops.get(crop_pred.lower(), "Standard irrigation method is sufficient.")
#             profit = lookup_profit_for_crop(crop_pred)

#             # Save to linked_tester_data.csv to allow farmer linking
#             header = ['name','phone', 'location', 'N', 'P', 'K', 'temperature', 'humidity',
#                       'ph', 'rainfall', 'crop', 'soil_type', 'season', 'water_level',
#                       'fertilizer_required', 'pest_present']
#             row = [name,'phone', location, N, P, K, temperature, humidity, ph, rainfall,
#                    crop_pred, soil_type, season, water_level, fertilizer_required, pest_present]
#             save_csv_row(LINKED_TESTER_FILE, header, row)

#             # Render tester report page (frontend expects these variables)
#             tester_report = f"Predicted most suitable crop: {crop_pred} (Estimated profit: {profit})"
#             return render_template(
#                 "tester_report.html",
#                 name=name,
#                 phone=phone,
#                 location=location,
#                 N=N, P=P, K=K,
#                 ph=ph, temperature=temperature, humidity=humidity, rainfall=rainfall,
#                 soil_type=soil_type, water_level=water_level, season=season,
#                 fertilizer=fertilizer_required, pest=pest_present,
#                 tester_report=tester_report
#             )
#     return render_template("tester.html")


# # Tester success page
# @app.route('/tester', methods=['GET', 'POST'])
# def tester():
#     if request.method == 'POST':
#         # Save tester data...
#         return render_template("tester_success.html")
#     return render_template("tester.html")

# #Tester report
# @app.route('/tester_report')
# def tester_report():
#     # Load latest tester data
#     df = pd.read_csv(os.path.join(BASE_DIR, "linked_tester_data.csv"), encoding="utf-8")
#     last_entry = df.iloc[-1].to_dict()
#     return render_template("tester_report.html", data=last_entry)

# # ========== Run ==========
# if __name__ == '__main__':
#     # debug=True for development; set to False in production
#     app.run(debug=True, host="0.0.0.0", port=5000)









from flask import Flask, request, render_template, redirect, url_for
import os, csv
import joblib
import pandas as pd
import requests
from flask import session
from deep_translator import GoogleTranslator

app = Flask(__name__)

# ========== Paths & config ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")
PROFIT_PATH = os.path.join(BASE_DIR, "profit_data.csv")
LINKED_TESTER_FILE = os.path.join(BASE_DIR, "linked_tester_data.csv")
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.csv")
FARMER_REQUESTS_FILE = os.path.join(BASE_DIR, "farmer_requests.csv")

# Load model and profit data
# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Place crop_model.pkl there.")

# model = joblib.load(MODEL_PATH)

#TEMPORATY CHANGE
if joblib and os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None   # dummy model for frontend testing


if os.path.exists(PROFIT_PATH):
    profit_df = pd.read_csv(PROFIT_PATH, encoding="utf-8")
else:
   # profit_df = pd.DataFrame(columns=["crop", "estimated_profit"])
   profit_df = None


OPENWEATHER_API_KEY = "eba7a9462af4cfa2bd8c3de9fbd5e887"


# ---------- Utilities ----------
def fetch_weather_for_location(location: str):
    default = (25.0, 60.0, 0.0)
    if not OPENWEATHER_API_KEY:
        return default
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={requests.utils.quote(location)}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        main = data.get("main", {})
        temp = main.get("temp", default[0])
        hum = main.get("humidity", default[1])
        rain = data.get("rain", {})
        rainfall = rain.get("1h", rain.get("3h", 0.0))
        return float(temp), float(hum), float(rainfall)
    except Exception:
        return default

def lookup_profit_for_crop(crop_name: str):
    if profit_df is None or profit_df.empty:
        return "N/A"
    row = profit_df[profit_df['crop'].astype(str).str.lower() == str(crop_name).lower()]
    if not row.empty:
        try:
            return int(row['estimated_profit'].values[0])
        except Exception:
            return row['estimated_profit'].values[0]
    return "N/A"

#--------language---------
app.secret_key="4d760f22493d0e0df77aa8f4375ff517"

def translate_text(text, lang):
    if not lang or lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=lang).translate(text)
    except Exception:
        return text

@app.template_filter('translate')
def translate_filter(text):
    lang = session.get('language', 'en')
    return translate_text(text, lang)

def translate_crop_name(crop_name: str, dest_lang: str):
    try:
        if not dest_lang or dest_lang == "en":
            return crop_name
        return GoogleTranslator(source="en", target=dest_lang).translate(crop_name)
    except Exception:
        return crop_name

def save_csv_row(filepath, header, row):
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

def get_irrigation_suggestion(crop_name, soil_type, water_requirement, root_depth):
    crop_name = crop_name.lower()

    # Example simple logic
    if water_requirement > 1200 or root_depth > 100:
        return "Drip irrigation is recommended"
    elif soil_type.lower() in ["sandy", "loamy"] and water_requirement < 800:
        return "Sprinkler irrigation is recommended"
    else:
        return "Surface irrigation is sufficient"

def evaluate_crops(crops, profit_df, soil_type="Loam", water_requirement=800, root_depth=50):
    results = []
    for crop in crops:
        profit = lookup_profit_for_crop(crop)
        irrigation = get_irrigation_suggestion(crop, soil_type, water_requirement, root_depth)
        results.append({
            "crop": crop,
            "profit": profit,
            "irrigation": irrigation
        })
    # Sort by profit
    results.sort(key=lambda x: x["profit"] if isinstance(x["profit"], (int, float)) else -1, reverse=True)
    return results

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")



#------farmer-report-------
# @app.route('/farmer_report', methods=['POST'])
# def farmer_report():
#     name = request.form.get('name', '').strip()
#     location = request.form.get('location', '').strip()
#     language = request.form.get('language', 'en').strip()

#     # Check if report exists
#     report_path = f"static/reports/{name}_report.html"  # adjust path
#     if os.path.exists(report_path):
#         # Report exists, render result.html or redirect to actual report
#         return render_template("result.html", name=name, location=location, language=language)
#     else:
#         # Report does not exist yet
#         return render_template("check_result.html", name=name)

#------farmer-report-------
@app.route('/farmer_report', methods=['POST'])
def farmer_report():
    name = request.form.get('name', '').strip()
    location = request.form.get('location', '').strip()
    language = request.form.get('language', 'en').strip()
    session['language']=language

    # ✅ Fetch weather here
    temp, hum, rain = fetch_weather_for_location(location)

    # Check if report exists
    report_path = f"static/reports/{name}_report.html"  # adjust path
    if os.path.exists(report_path):
        # Report exists, render result.html
        return render_template(
            "result.html",
            name=name,
            location=location,
            language=language,
            temperature=temp,
            humidity=hum,
            rainfall=rain
        )
    else:
        # Report does not exist yet
        return render_template(
            "check_result.html",
            name=name,
            temperature=temp,
            humidity=hum,
            rainfall=rain
        )



#-------------farmer flow----------
@app.route('/farmer', methods=['GET', 'POST'])
def farmer():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        location = request.form.get('location', '').strip()
        phone = request.form.get('phone', '').strip()
        language = request.form.get('language', '').strip()
        session['language']=language

        header = ['Name', 'Location', 'Phone', 'Language']
        row = [name, location, phone, language]
        save_csv_row(FARMER_REQUESTS_FILE, header, row)

        # Check if report exists
        report_exists = os.path.exists(os.path.join("templates", "result.html"))  # adjust path
        return render_template(
            "thankyou.html",
            name=name,
            location=location,
            phone=phone,
            language=language,
            report_exists=report_exists
        )
    return render_template("farmer.html")
    


@app.route('/result')
def result():
    name = request.args.get('name')
    phone = request.args.get('phone')
    location = request.args.get('location')
    language = request.args.get('language')

    try:
        df = pd.read_csv(FARMER_REQUESTS_FILE)
        # check if this farmer exists in tester data
        matched = df[
            (df['Name'].astype(str).str.lower() == name.lower()) &
            (df['Phone'].astype(str).str.lower() == phone.lower()) &
            (df['Location'].astype(str).str.lower() == location.lower())
        ]
    except Exception:
        matched = pd.DataFrame()  # no data at all

    if not matched.empty:
        # farmer exists in tester records
        return render_template("result.html",
                               name=name,
                               location=location,
                               phone=phone,
                               )
    else:
        # farmer not found → show check_result
        return render_template("check_result.html",
                               name=name,
                               location=location,
                               phone=phone,
                               )

# @app.route('/result')
# def result():
#     name = request.args.get('name')
#     phone = request.args.get('phone')
#     location = request.args.get('location')
#     language = request.args.get('language')
#     session['language']=language
#     # Load and display the result for this farmer
#     report_path = os.path.join("templates","result.html")
#     if os.path.exists(report_path):
#         return render_template("result.html",
#                                name=name,
#                                location=location,
#                                phone=phone,
#                                language=language)
#     else:
#         return render_template("check_result.html",
#                                name=name,
#                                location=location,
#                                phone=phone,
#                                language=language)
#     return render_template('result.html', name=name,phone=phone, location=location, language=language)


# ---------------- FEEDBACK FLOW ----------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form['message']
        # Save feedback to CSV or database here
        return redirect(url_for('feedback_submit'))
    return render_template('feedback.html')


@app.route('/feedback_submit')
def feedback_submit():
    return render_template('feedback_submit.html')


# -------- Tester Flow --------
@app.route('/tester', methods=['GET', 'POST'])
def tester():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            location = request.form.get('location', '').strip()
            language = request.form.get('language', 'en').strip()
            session['language'] = language
            N = float(request.form.get('N', 0))
            P = float(request.form.get('P', 0))
            K = float(request.form.get('K', 0))
            temperature = float(request.form.get('temperature', ''))
            humidity = float(request.form.get('humidity', ''))
            ph = float(request.form.get('ph', ''))
            rainfall = float(request.form.get('rainfall', ''))
            soil_type = request.form.get('soil_type', '')
            season = request.form.get('season', '')
            water_level = request.form.get('water_level', '')
            fertilizer_required = request.form.get('fertilizer') or request.form.get('fertilizer_required') or ''
            pest_present = request.form.get('pest') or request.form.get('pest_present') or ''

            # ✅ Predict using ML model if available
            if model:
                input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
                probs = model.predict_proba(input_data)[0]
                classes = model.classes_

                # Get top 3 crops
                top_indices = probs.argsort()[-3:][::-1]
                top_crops = [classes[i] for i in top_indices]
            else:
                top_crops = ["Rice", "Wheat", "Maize"]  # fallback

            # ✅ Evaluate top crops with profit + irrigation
            crop_results = evaluate_crops(top_crops, profit_df, soil_type, water_level, ph)
            most_profitable_crop = crop_results[0]["crop"]

            # ✅ Save submission to CSV
            header = ['name','phone','location','N','P','K','temperature','humidity',
                    'ph','rainfall','predicted_crops','soil_type','season','water_level',
                    'fertilizer_required','pest_present']
            row = [name, phone, location, N, P, K, temperature, humidity, ph, rainfall,
                ", ".join(top_crops), soil_type, season, water_level, fertilizer_required, pest_present]
            save_csv_row(LINKED_TESTER_FILE, header, row)

            # ✅ Fetch weather info for tester
            temp_now, hum_now, rain_now = fetch_weather_for_location(location)

            # ✅ Render success page
            return render_template("tester_success.html",
                                name=name,
                                phone=phone,
                                location=location,
                                top_crops=crop_results,
                                most_profitable=most_profitable_crop,
                                temperature=temp_now,
                                humidity=hum_now,
                                rainfall=rain_now)

        except Exception as e:
            return f"Error processing tester form: {e}"

    return render_template("tester.html")


@app.route('/tester_report', methods=['POST'])
def tester_report():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    location = request.form.get('location', '').strip()
    language = request.form.get('language', 'en').strip()
    session['language'] = language
    # ✅ Fetch weather info
    temp_now, hum_now, rain_now = fetch_weather_for_location(location)

    # # Dummy data to simulate tester report
    # dummy_data = {
    #     "name": name if name else "Test User",
    #     "Phno": phone if phone else "1234567890",
    #     "location": location if location else "Bangalore",
    #     "N": 60,
    #     "P": 23,
    #     "K": 42,
    #     "temperature": temp_now,
    #     "humidity": hum_now,
    #     "ph": 6.5,
    #     "rainfall": rain_now,
    #     "soil_type": "Red",
    #     "season": "Kharif",
    #     "water_level": "Medium",
    #     "fertilizer": "Yes",
    #     "pest": "No",
    #     "tester_report": "Predicted crop: Rice (Estimated profit: 5000)"
    # }

    # return render_template("tester_report.html", **dummy_data)
   
    df = pd.read_csv(LINKED_TESTER_FILE, encoding='utf-8')

    matched = df[
        (df['name'].astype(str).str.lower() == name.lower()) &
        (df['phone'].astype(str).str.lower() == phone.lower()) &
        (df['location'].astype(str).str.lower() == location.lower())
    ]

    if matched.empty:
        return "⚠️ No tester report found."

    last_entry = matched.iloc[-1].to_dict()

    # Build tester report message
    tester_report_msg = f"Predicted most suitable crop: {last_entry.get('crop', 'Unknown')} (Estimated profit: {lookup_profit_for_crop(last_entry.get('crop', ''))})"

    return render_template("tester_report.html",
                           name=last_entry.get('name'),
                           Phno=last_entry.get('phone'),
                           location=last_entry.get('location'),
                           N=last_entry.get('N'),
                           P=last_entry.get('P'),
                           K=last_entry.get('K'),
                           ph=last_entry.get('ph'),
                           temperature=last_entry.get('temperature'),
                           humidity=last_entry.get('humidity'),
                           rainfall=last_entry.get('rainfall'),
                           soil_type=last_entry.get('soil_type'),
                           water_level=last_entry.get('water_level'),
                           season=last_entry.get('season'),
                           fertilizer=last_entry.get('fertilizer_required'),
                           pest=last_entry.get('pest_present'),
                           tester_report=tester_report_msg
                           )
# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
