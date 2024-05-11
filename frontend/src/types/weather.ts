interface WeatherData {
  timestamp: string;
  outdoor_temp: number;
  outdoor_feels_like: number;
  outdoor_pressure: number;
  outdoor_humidity: number;
  outdoor_weather: string;
  outdoor_description: string;
  outdoor_pm25: number;
  outdoor_pm10: number;
  indoor_temp: number;
  indoor_light: number;
}

interface IndoorWeatherData {
  avg_indoor_temp: number;
  avg_indoor_light: number;
}

interface WeatherData {
  avg_outdoor_temp: number;
  avg_outdoor_feels_like: number;
  avg_outdoor_pressure: number;
  avg_outdoor_humidity: number;
  avg_outdoor_pm25: number;
  avg_outdoor_pm10: number;
}

interface IndoorPredictData {
  timestamp: string;
  indoor_temp: number;
  outdoor_temp: number;
}
