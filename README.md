# Smart Crop Recommendation System

An AI-powered web application for Tamil Nadu crop planning. The platform recommends the best crop from location, soil type, season, and land area, fetches weather through OpenWeatherMap, estimates yield and profit, suggests a sowing month, and stores every prediction in MongoDB Atlas.

## Features

- Professional government-style agriculture portal UI
- Tamil and English language switcher
- Weather-aware crop recommendation workflow
- Flask backend with modular services and routes
- Random Forest classifier using Scikit-learn
- OpenWeatherMap temperature, humidity, and rainfall integration
- MongoDB Atlas prediction history with filters and CSV export
- Responsive pages for desktop, tablet, and mobile
- Input validation, logging, and environment-based configuration

## Folder Structure

```text
SmartCropRecommendation/
  app.py
  config.py
  requirements.txt
  README.md
  .gitignore
  .env
  data/
    raw/
    processed/
  models/
    train_model.py
    predict.py
    model.pkl
    label_encoder.pkl
  services/
    weather_service.py
    prediction_service.py
    profit_service.py
  database/
    mongodb.py
  routes/
    main_routes.py
  templates/
    layout.html
    index.html
    result.html
    history.html
    about.html
    contact.html
    404.html
    500.html
  static/
    css/
      style.css
      responsive.css
      animations.css
    js/
      script.js
      validation.js
    images/
    icons/
  utils/
    helpers.py
    validators.py
    constants.py
  logs/
    app.log
  tests/
    test_api.py
    test_database.py
    test_model.py
```

`model.pkl` and `label_encoder.pkl` are generated after training.

## Technology Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript, Font Awesome, Google Fonts
- Backend: Python Flask
- Machine Learning: Scikit-learn, Joblib, Pandas
- Database: MongoDB Atlas with PyMongo
- API: OpenWeatherMap
- Configuration: python-dotenv
- Testing: Pytest

## Installation

```bash
cd SmartCropRecommendation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Update `.env`:

```env
SECRET_KEY=your-secure-secret
OPENWEATHER_API_KEY=your-openweathermap-key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=smart_crop_db
MONGO_COLLECTION=predictions
FLASK_DEBUG=True
```

The app can run without these keys for local UI testing. Weather uses regional fallback values and database writes are skipped until MongoDB is configured.

## Train the Model

```bash
python models/train_model.py
```

This creates a compact processed training dataset when one is not present, trains a Random Forest classifier, and saves:

- `models/model.pkl`
- `models/label_encoder.pkl`

## How to Run

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## MongoDB Setup

1. Create a MongoDB Atlas cluster.
2. Create a database user and allow your IP address.
3. Copy the connection string into `MONGO_URI`.
4. The app uses database `smart_crop_db` and collection `predictions`.
5. New recommendations are stored automatically after prediction.

## OpenWeatherMap API Setup

1. Create an account at OpenWeatherMap.
2. Generate an API key.
3. Add it to `OPENWEATHER_API_KEY` in `.env`.
4. The weather service fetches temperature, humidity, and recent rainfall for the selected district.

## Screenshots

Add screenshots here after running the app:

- Home and recommendation form
- Result dashboard
- History table
- Mobile view

## Testing

```bash
pytest
```

## Future Scope

- Add real government datasets and district-level soil maps
- Add multilingual Tamil and English support
- Integrate market price APIs
- Add farmer login and advisory notifications
- Improve model training with larger historical climate and yield data
- Add explainable AI notes for each recommendation

## License

This project is provided for educational and product prototype use. Review and adapt licensing before public deployment.
