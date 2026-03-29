import AlertBanner from '../components/dashboard/AlertBanner';
import StatusBar from '../components/dashboard/StatusBar';
import HomeLayout from '../components/layout/HomeLayout';
// import MainDashboard from '../components/dashboard/MainDashboard';
export default function Dashboard() {
  return (
    <HomeLayout headerName="Dashboard">
      <AlertBanner>ALERT: Temperature 34.2°C — above safe threshold in Living Room</AlertBanner>
      {/* <MainDashboard /> */}
      <StatusBar />
    </HomeLayout>
  )
}