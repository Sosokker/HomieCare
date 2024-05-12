import { useEffect, useState } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';

import Loader from './common/Loader';
import PageTitle from './components/PageTitle';
import Statistic from './pages/Dashboard/Statistic';
import Alerts from './pages/UiElements/Alerts';
import Buttons from './pages/UiElements/Buttons';
import Camera from './pages/Camera';

function App() {
  const [loading, setLoading] = useState<boolean>(true);
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  return loading ? (
    <Loader />
  ) : (
    <>
      <Routes>
        <Route
          index
          element={
            <>
              <PageTitle title="Statistic Dashboard" />
              <Statistic />
            </>
          }
        />
        <Route
          path="/camera"
          element={
            <>
              <PageTitle title="Camera" />
              <Camera />
            </>
          }
        />
        <Route
          path="/snapshot"
          element={
            <>
              <PageTitle title="Snapshot" />
              <Alerts />
            </>
          }
        />
      </Routes>
    </>
  );
}

export default App;
