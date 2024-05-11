import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import DefaultLayout from '../layout/DefaultLayout';

const Camera = () => {
  return (
    <DefaultLayout>
      <Breadcrumb pageName="Camera" />

      <div className="overflow-hidden rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        Camera here
      </div>
    </DefaultLayout>
  );
};

export default Camera;
