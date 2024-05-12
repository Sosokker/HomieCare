import React, { useEffect, useState } from 'react';
import { fetchCameraSnapshotUrls } from '../api/SnapshotData';
import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import DefaultLayout from '../layout/DefaultLayout';

const Snapshot: React.FC = () => {
  const [imageUrls, setImageUrls] = useState<string[]>([]);
  const [selectedInterval, setSelectedInterval] = useState<string>('week');

  useEffect(() => {
    const fetchUrls = async () => {
      const urls = await fetchCameraSnapshotUrls(selectedInterval);
      if (urls) {
        setImageUrls(urls);
      } else {
        console.error('Failed to fetch image URLs');
      }
    };

    fetchUrls();
  }, [selectedInterval]);

  const handleIntervalChange = (interval: string) => {
    setSelectedInterval(interval);
  };

  return (
    <DefaultLayout>
      <Breadcrumb pageName="Snapshot" />
      <div>
        <div className="flex space-x-4 mb-4">
          <button
            className={`${
              selectedInterval === 'today'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-300'
            } px-4 py-2 rounded`}
            onClick={() => handleIntervalChange('today')}
          >
            Today
          </button>
          <button
            className={`${
              selectedInterval === 'week'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-300'
            } px-4 py-2 rounded`}
            onClick={() => handleIntervalChange('week')}
          >
            Week
          </button>
          <button
            className={`${
              selectedInterval === 'month'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-300'
            } px-4 py-2 rounded`}
            onClick={() => handleIntervalChange('month')}
          >
            Month
          </button>
          <button
            className={`${
              selectedInterval === 'all'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-300'
            } px-4 py-2 rounded`}
            onClick={() => handleIntervalChange('all')}
          >
            All
          </button>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {imageUrls.map((url, index) => (
            <img
              key={index}
              src={url}
              alt={`Image ${index}`}
              className="w-full h-auto"
            />
          ))}
        </div>
      </div>
    </DefaultLayout>
  );
};

export default Snapshot;
