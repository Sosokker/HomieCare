import joblib


class XgboostIndoorModel:
    MODEL_PATH = 'xgboost_model.pkl'

    def __init__(self):
        self.__model = joblib.load(self.MODEL_PATH)

    def predict(self, X: list) -> float:
        """
        Predict the indoor temperature based on the input features
        Input order : ['outdoor_temp', 'outdoor_feels_like', 'outdoor_pressure',
       'outdoor_humidity', 'outdoor_pm25', 'outdoor_pm10']
        """
        if len(X) != 6:
            raise ValueError(f"Expected 6 features, got {len(X)}")
        
        return self.__model.predict([X])[0]