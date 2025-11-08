import React, { useState, useEffect } from 'react';
import { EdgeQIProvider } from './contexts/EdgeQIContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/pages/Dashboard';
import EdgeNodes from './components/pages/EdgeNodes';
import Detection from './components/pages/Detection';
import Analytics from './components/pages/Analytics';
import Consensus from './components/pages/Consensus';
import Logs from './components/pages/Logs';
import Settings from './components/pages/Settings';
import CamerasPage from './pages/CamerasPage';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'nodes':
        return <EdgeNodes />;
      case 'cameras':
        return <CamerasPage />;
      case 'detection':
        return <Detection />;
      case 'analytics':
        return <Analytics />;
      case 'consensus':
        return <Consensus />;
      case 'logs':
        return <Logs />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <EdgeQIProvider>
      <div className="flex h-screen bg-black text-white overflow-hidden">
        <Sidebar
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
          collapsed={sidebarCollapsed}
          setCollapsed={setSidebarCollapsed}
        />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header
            currentPage={currentPage}
            toggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
          
          <main className="flex-1 overflow-y-auto overflow-x-hidden">
            <div className="max-w-[1920px] mx-auto p-6">
              {renderPage()}
            </div>
          </main>
        </div>
      </div>
    </EdgeQIProvider>
  );
}

export default App;
