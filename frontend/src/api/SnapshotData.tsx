import axios from 'axios';

const fetchCameraSnapshotUrls = async (
  interval: string,
): Promise<string[] | null> => {
  try {
    const response = await axios.get<string[]>(
      `http://127.0.0.1:8000/api/v1/camera/snapshot/${interval}`,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching camera snapshot URLs:', error);
    return null;
  }
};

export { fetchCameraSnapshotUrls };
