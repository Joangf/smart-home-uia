import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./services/AuthProvider";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./services/ProtectedRoute";
import NotiProvider from "./services/NotiProvider";
import ToastNoti from "./components/ui/ToastNoti";
export default function App() {
  return (
    <BrowserRouter>
      <NotiProvider>
        <ToastNoti /> {/* Global notification component */}
        <AuthProvider>
          <Routes>
            {/* Public */}
            <Route path="/login" element={<Login />} />
            {/* Protected */}
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              {/*Placeholder for future routes */}
              <Route path="/devices" element={<Dashboard />} />
              <Route path="/environment" element={<Dashboard />} />
              <Route path="/security" element={<Dashboard />} />
              <Route path="/notifications" element={<Dashboard />} />
              <Route path="/automation" element={<Dashboard />} />
              <Route path="/management" element={<Dashboard />} />
            </Route>
          </Routes>
        </AuthProvider>
      </NotiProvider>
    </BrowserRouter>
  );
}
