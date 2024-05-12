import axios from 'axios';

const fetchRecommendation = async (
  data: HealthData,
): Promise<RecommendationData[] | null> => {
  try {
    const response = await axios.post<RecommendationData[]>(
      'http://127.0.0.1:8000/api/v1/recommend/recommendation/',
      data,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendation:', error);
    return null;
  }
};

export default fetchRecommendation;
