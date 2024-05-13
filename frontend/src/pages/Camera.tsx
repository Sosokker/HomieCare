import React, { useEffect, useRef, useState } from 'react';
import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import DefaultLayout from '../layout/DefaultLayout';
import LoadingAnimation from '../components/LoadingAnimation';

const Camera = () => {
  const webSocketRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [connectionError, setConnectionError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [cameras, setCameras] = useState<
    { camera_id: number; link: string; status: boolean }[]
  >([]);
  const [selectedCamera, setSelectedCamera] = useState<number | null>(null);

  useEffect(() => {
    // Fetch cameras data from the API
    const fetchCameras = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/api/v1/camera/list',
        );
        const data = await response.json();
        setCameras(data);
      } catch (error) {
        console.error('Error fetching cameras:', error);
      }
    };

    fetchCameras();
  }, []);

  const connectWebSocket = () => {
    if (selectedCamera !== null) {
      const selectedCameraData = cameras.find(
        (camera) => camera.camera_id === selectedCamera,
      );
      if (selectedCameraData && selectedCameraData.status) {
        setLoading(true);
        const websocketUrl = `ws://127.0.0.1:8000/api/v1/camera/ws/${selectedCamera}`;
        webSocketRef.current = new WebSocket(websocketUrl);

        webSocketRef.current.onmessage = (event) => {
          setLoading(false);
          const blob = new Blob([event.data], { type: 'image/png' });
          const imageUrl = URL.createObjectURL(blob);

          const image = new Image();
          image.onload = () => {
            if (canvasRef.current) {
              const context = canvasRef.current.getContext('2d');
              if (context) {
                context.drawImage(
                  image,
                  0,
                  0,
                  canvasRef.current.width,
                  canvasRef.current.height,
                );
              }
            }
          };
          image.src = imageUrl;
        };

        webSocketRef.current.onopen = () => {
          console.log('WebSocket connected');
          setConnectionError(false);
        };

        webSocketRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionError(true);
          setLoading(false);
        };

        webSocketRef.current.onclose = () => {
          console.log('WebSocket closed');
          setLoading(false);
        };
      }
    }
  };

  const handleCameraChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = parseInt(event.target.value, 10);
    setSelectedCamera(selectedValue);
  };

  const handleClearConnection = () => {
    if (webSocketRef.current?.readyState === WebSocket.OPEN) {
      webSocketRef.current.close();
    }
    setSelectedCamera(null);
  };

  return (
    <DefaultLayout>
      <Breadcrumb pageName="Camera" />

      <div className="overflow-hidden rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex justify-between items-center p-4">
          <select
            onChange={handleCameraChange}
            value={selectedCamera || ''}
            className="border border-gray-300 rounded-md px-3 py-1 mr-3 focus:outline-none"
          >
            <option value="">Select Camera</option>
            {cameras.map((camera) => (
              <option
                key={camera.camera_id}
                value={camera.camera_id}
                disabled={!camera.status}
              >
                {`Camera ${camera.camera_id}${camera.status ? '' : ' (Not available)'}`}
              </option>
            ))}
          </select>
          <div className="grid-cols-3 gap-4">
            <button
              onClick={handleClearConnection}
              disabled={selectedCamera === null || !webSocketRef.current}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mx-2"
            >
              Clear Connection
            </button>
            <button
              onClick={connectWebSocket}
              disabled={selectedCamera === null || loading}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Start Connection
            </button>
          </div>
        </div>
        {selectedCamera !== null && !loading && (
          <canvas
            ref={canvasRef}
            width={640}
            height={480}
            className="w-full h-full"
          ></canvas>
        )}
        {loading && <LoadingAnimation />}
      </div>
    </DefaultLayout>
  );
};

export default Camera;
