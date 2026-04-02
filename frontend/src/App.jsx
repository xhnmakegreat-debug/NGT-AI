import Dashboard from './components/Dashboard/Dashboard.jsx';
import LoginPanel from './components/Auth/LoginPanel.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';
import { LanguageProvider } from './i18n/LanguageContext.jsx';

function AppContent() {
  const { isAuthenticated } = useAuth();

  return (
    <>
      {!isAuthenticated && <LoginPanel />}
      <Dashboard />
    </>
  );
}

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;
