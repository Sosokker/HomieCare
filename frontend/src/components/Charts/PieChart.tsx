import { ApexOptions } from 'apexcharts';
import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';

interface ChartData {
  action: string;
  count: number;
  percentage: number;
}

const options: ApexOptions = {
  chart: {
    fontFamily: 'Satoshi, sans-serif',
    type: 'donut',
  },
  colors: ['#3C50E0', '#6577F3', '#8FD0EF', '#0FADCF'],
  labels: ['Sitting', 'Walking', 'Standing', 'Unknown'],
  legend: {
    show: false,
    position: 'bottom',
  },

  plotOptions: {
    pie: {
      donut: {
        size: '65%',
        background: 'transparent',
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 2600,
      options: {
        chart: {
          width: 380,
        },
      },
    },
    {
      breakpoint: 640,
      options: {
        chart: {
          width: 200,
        },
      },
    },
  ],
};

const PieChart: React.FC = () => {
  const [chartData, setChartData] = useState<ChartData[]>([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/action/week');
      const data: ActionData[] = await response.json();

      const actionCounts: { [key: string]: number } = {};
      data.forEach((item) => {
        actionCounts[item.action] = (actionCounts[item.action] || 0) + 1;
      });

      const totalCount = data.length;
      const chartData = Object.keys(actionCounts).map((action) => ({
        action,
        count: actionCounts[action],
        percentage: (actionCounts[action] / totalCount) * 100,
      }));

      setChartData(chartData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="sm:px-7.5 col-span-12 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-5">
      <div className="mb-3 justify-between gap-4 sm:flex">
        <div>
          <h5 className="text-xl font-semibold text-black dark:text-white">
            Action Analysis
          </h5>
        </div>
      </div>

      <div className="mb-2">
        <div id="chartThree" className="mx-auto flex justify-center">
          <ReactApexChart
            options={options}
            series={chartData.map((item) => item.count)}
            type="donut"
          />
        </div>
      </div>

      <div className="-mx-8 flex flex-wrap items-center justify-center gap-y-3">
        {chartData.map((item, index) => (
          <div key={index} className="sm:w-1/2 w-full px-8">
            <div className="flex w-full items-center">
              <span className="mr-2 block h-3 w-full max-w-3 rounded-full bg-primary"></span>
              <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
                <span>{item.action}</span>
                <span>{item.count} times</span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PieChart;
