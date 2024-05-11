import React from 'react';
import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import LineChart from '../components/Charts/LineChart';
import PieChart from '../components/Charts/PieChart';
import BarChart from '../components/Charts/BarChart';
import DefaultLayout from '../layout/DefaultLayout';

const Chart: React.FC = () => {
  return (
    <DefaultLayout>
      <Breadcrumb pageName="Chart" />

      <div className="grid grid-cols-12 gap-4 md:gap-6 2xl:gap-7.5">
        <LineChart />
        <BarChart />
        <PieChart />
      </div>
    </DefaultLayout>
  );
};

export default Chart;
