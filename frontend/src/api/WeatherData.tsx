import axios from 'axios';

const fetchWeatherDataList = async (
  days: number,
): Promise<WeatherData[] | null> => {
  try {
    const response = await axios.get<WeatherData[]>(
      `http://127.0.0.1:8000/api/v1/weather/${days}`,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching weather data list:', error);
    return null;
  }
};

const fetchOutdoorWeatherData = async (
  days: number,
): Promise<WeatherData | null> => {
  try {
    const response = await axios.get<WeatherData>(
      `http://127.0.0.1:8000/api/v1/weather/average/outdoor/${days}`,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    return null;
  }
};

const fetchIndoorWeatherData = async (
  days: number,
): Promise<IndoorWeatherData | null> => {
  try {
    const response = await axios.get<IndoorWeatherData>(
      `http://127.0.0.1:8000/api/v1/weather/average/indoor/${days}`,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching indoor weather data:', error);
    return null;
  }
};

export {
  fetchWeatherDataList,
  fetchOutdoorWeatherData,
  fetchIndoorWeatherData,
};
