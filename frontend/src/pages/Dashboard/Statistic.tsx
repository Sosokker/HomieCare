import React from 'react';
import CardDataStats from '../../components/CardDataStats';
import LineChart from '../../components/Charts/LineChart';
import PieChart from '../../components/Charts/PieChart';
import BarChart from '../../components/Charts/BarChart';
import DefaultLayout from '../../layout/DefaultLayout';
import { FaTemperatureHigh } from 'react-icons/fa';
import { WiHumidity } from 'react-icons/wi';
import { PiFactoryBold } from 'react-icons/pi';
import { TbBuildingFactory } from 'react-icons/tb';

const Statistic: React.FC = () => {
  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        <CardDataStats
          title="Average Temperature"
          total="$3.456K"
          rate="0.43%"
          levelUp
        >
          <FaTemperatureHigh />
        </CardDataStats>
        <CardDataStats
          title="Average Humidity"
          total="$45,2K"
          rate="4.35%"
          levelUp
        >
          <WiHumidity />
        </CardDataStats>
        <CardDataStats title="Average PM2.5" total="2.450" rate="2.59%" levelUp>
          <PiFactoryBold />
        </CardDataStats>
        <CardDataStats
          title="Average PM10"
          total="3.456"
          rate="0.95%"
          levelDown
        >
          <TbBuildingFactory />
        </CardDataStats>
      </div>

      <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
        <LineChart />
        <BarChart />
        <PieChart />
      </div>
    </DefaultLayout>
  );
};

export default Statistic;
