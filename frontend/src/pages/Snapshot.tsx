import React, { useEffect, useState } from 'react';
import { fetchCameraSnapshotUrls } from '../api/SnapshotData';
import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import DefaultLayout from '../layout/DefaultLayout';

const Snapshot: React.FC = () => {
  const [imageUrls, setImageUrls] = useState<string[]>([]);

  useEffect(() => {
    const fetchUrls = async () => {
      const urls = await fetchCameraSnapshotUrls('week');
      if (urls) {
        setImageUrls(urls);
      } else {
        console.error('Failed to fetch image URLs');
      }
    };

    fetchUrls();
  }, []);

  return (
    <DefaultLayout>
      <Breadcrumb pageName="Snapshot" />
      <div>
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
