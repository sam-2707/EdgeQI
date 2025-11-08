import React from 'react';
import { Menu, Bell, AlertCircle, CheckCircle, XCircle, X } from 'lucide-react';
import { useEdgeQI } from '../contexts/EdgeQIContext';

const Header = ({ currentPage, toggleSidebar }) => {
  const { connected, alerts, dismissAlert } = useEdgeQI();
  const [showAlerts, setShowAlerts] = React.useState(false);

  const pageTitle = {
    dashboard: 'Dashboard',
    nodes: 'Edge Nodes',
    detection: 'Object Detection',
    analytics: 'Analytics & Reports',
    consensus: 'Consensus Protocol',
    logs: 'System Logs',
    settings: 'Settings',
  }[currentPage] || 'EDGE-QI';

  const unreadAlerts = alerts.filter((a) => !a.read).length;

  return (
    <header className="h-16 bg-neutral-950 border-b border-neutral-800 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="lg:hidden p-2 rounded-md hover:bg-white/5 transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <div>
          <h2 className="text-xl font-bold">{pageTitle}</h2>
          <p className="text-xs text-neutral-500">
            Real-time Smart City Monitoring
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Connection Status */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-neutral-900 border border-neutral-800">
          <div
            className={`w-2 h-2 rounded-full ${
              connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
            }`}
          />
          <span className="text-xs font-medium">
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>

        {/* Alerts */}
        <div className="relative">
          <button
            onClick={() => setShowAlerts(!showAlerts)}
            className="relative p-2 rounded-md hover:bg-white/5 transition-colors"
          >
            <Bell className="w-5 h-5" />
            {unreadAlerts > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                {unreadAlerts > 9 ? '9+' : unreadAlerts}
              </span>
            )}
          </button>

          {/* Alerts Dropdown */}
          {showAlerts && (
            <>
              <div
                className="fixed inset-0 z-40"
                onClick={() => setShowAlerts(false)}
              />
              <div className="absolute right-0 mt-2 w-96 card p-4 z-50 max-h-[32rem] overflow-y-auto">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold">Alerts</h3>
                  <button
                    onClick={() => setShowAlerts(false)}
                    className="p-1 rounded hover:bg-white/5"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                {alerts.length === 0 ? (
                  <p className="text-sm text-neutral-500 text-center py-8">
                    No alerts
                  </p>
                ) : (
                  <div className="space-y-2">
                    {alerts.map((alert) => (
                      <div
                        key={alert.id}
                        className="p-3 rounded-lg bg-neutral-900 border border-neutral-800 flex gap-3"
                      >
                        <div className="flex-shrink-0 mt-0.5">
                          {alert.type === 'error' && (
                            <XCircle className="w-5 h-5 text-red-400" />
                          )}
                          {alert.type === 'warning' && (
                            <AlertCircle className="w-5 h-5 text-yellow-400" />
                          )}
                          {alert.type === 'success' && (
                            <CheckCircle className="w-5 h-5 text-green-400" />
                          )}
                          {alert.type === 'info' && (
                            <Bell className="w-5 h-5 text-blue-400" />
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">{alert.message}</p>
                          <p className="text-xs text-neutral-500 mt-1">
                            {new Date(alert.timestamp).toLocaleTimeString()}
                          </p>
                        </div>
                        <button
                          onClick={() => dismissAlert(alert.id)}
                          className="flex-shrink-0 p-1 rounded hover:bg-white/5"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
