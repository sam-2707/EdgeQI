import React from 'react';
import {
  LayoutDashboard,
  Network,
  Camera,
  BarChart3,
  GitBranch,
  FileText,
  Settings,
  ChevronLeft,
  ChevronRight,
  Cpu,
  Video,
} from 'lucide-react';

const Sidebar = ({ currentPage, setCurrentPage, collapsed, setCollapsed }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'nodes', label: 'Edge Nodes', icon: Network },
    { id: 'cameras', label: 'Live Cameras', icon: Video },
    { id: 'detection', label: 'Detection', icon: Camera },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'consensus', label: 'Consensus', icon: GitBranch },
    { id: 'logs', label: 'System Logs', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside
      className={`${
        collapsed ? 'w-20' : 'w-64'
      } bg-neutral-950 border-r border-neutral-800 flex flex-col transition-all duration-300 ease-in-out`}
    >
      {/* Logo & Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-neutral-800">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <Cpu className="w-5 h-5 text-black" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">EDGE-QI</h1>
              <p className="text-[10px] text-neutral-500 uppercase tracking-wider">
                Smart City
              </p>
            </div>
          </div>
        )}
        {collapsed && (
          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center mx-auto">
            <Cpu className="w-5 h-5 text-black" />
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-1 px-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;

            return (
              <li key={item.id}>
                <button
                  onClick={() => setCurrentPage(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md transition-all duration-200 ${
                    isActive
                      ? 'bg-white text-black'
                      : 'text-neutral-400 hover:text-white hover:bg-white/5'
                  }`}
                  title={collapsed ? item.label : ''}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {!collapsed && (
                    <span className="text-sm font-medium">{item.label}</span>
                  )}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Toggle Button */}
      <div className="p-2 border-t border-neutral-800">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-md text-neutral-400 hover:text-white hover:bg-white/5 transition-all duration-200"
        >
          {collapsed ? (
            <ChevronRight className="w-5 h-5" />
          ) : (
            <>
              <ChevronLeft className="w-5 h-5" />
              <span className="text-sm font-medium">Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
