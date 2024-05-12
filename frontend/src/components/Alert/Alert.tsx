import React, { useEffect, useState } from 'react';
import DangerAlert from './DangerAlert';
import GoodAlert from './GoodAlert';
import WarningAlert from './WarningAlert';
import fetchRecommendation from '../../api/RecommendData';

const Alert: React.FC<HealthData> = ({
  indoor_temp,
  outdoor_temp,
  outdoor_pm25,
  outdoor_pm10,
  outdoor_humidity,
}) => {
  const [recommendation, setRecommendation] = useState<
    string | null | undefined
  >(null);
  const [message, setMessage] = useState<string | undefined>('');

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchRecommendation({
        indoor_temp: indoor_temp,
        outdoor_temp: outdoor_temp,
        outdoor_pm25: outdoor_pm25,
        outdoor_pm10: outdoor_pm10,
        outdoor_humidity: outdoor_humidity,
      });

      if (data && data.length > 0) {
        // priority: danger > warning > good
        for (let i = 0; i < data.length; i++) {
          if (data[i].status === 'danger' || data[i].status === 'warning') {
            setRecommendation(data[i].status);
            setMessage(data[i].recommendation);
            return;
          }
        }
      }
    };

    fetchData();
  }, []);

  if (recommendation === 'good') {
    return <GoodAlert message={message} />;
  } else if (recommendation === 'warning') {
    return <WarningAlert message={message} />;
  } else if (recommendation === 'danger') {
    return <DangerAlert message={message} />;
  } else {
    return <GoodAlert message="No tips today" />;
  }
};

export default Alert;
