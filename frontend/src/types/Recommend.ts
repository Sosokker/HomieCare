interface HealthData {
  indoor_temp: number | undefined;
  outdoor_temp: number | undefined;
  outdoor_pm25: number | undefined;
  outdoor_pm10: number | undefined;
  outdoor_humidity: number | undefined;
}

interface RecommendationData {
  timestamp?: Date;
  recommendation?: string;
  status?: string;
}
