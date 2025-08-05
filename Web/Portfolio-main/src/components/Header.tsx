import React, { useState, useEffect } from 'react';
import { Menu, X, Sparkles } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('home');

  const navItems = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Skills', href: '#skills' },
    { name: 'Projects', href: '#projects' },
    { name: 'Contact', href: '#contact' }
  ];

  useEffect(() => {
    const handleScroll = () => {
      const sections = navItems.map(item => item.href.substring(1));
      const scrollPosition = window.scrollY + 100;

      for (const section of sections) {
        const element = document.getElementById(section);
        if (element) {
          const offsetTop = element.offsetTop;
          const offsetHeight = element.offsetHeight;

          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [navItems]);

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-br from-black/90 via-gray-900/90 to-black/90 backdrop-blur-xl border-b border-gray-700/50 shadow-2xl">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-4 left-4 w-32 h-32 bg-gray-500/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-8 right-8 w-32 h-32 bg-gray-400/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>

        {/* 3D Floating Cubes */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`cube-${i}`}
            className="absolute w-8 h-8 bg-gradient-to-br from-gray-300/20 to-gray-500/20 transform-gpu animate-cube-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${4 + Math.random() * 3}s`,
              transform: `rotateX(${Math.random() * 360}deg) rotateY(${Math.random() * 360}deg) rotateZ(${Math.random() * 360}deg)`
            }}
          />
        ))}

        {/* 3D Geometric Shapes */}
        {[...Array(3)].map((_, i) => (
          <div
            key={`geo-${i}`}
            className="absolute w-10 h-10 bg-gradient-to-br from-gray-300/15 to-gray-500/15 transform-gpu animate-geometric-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 4}s`,
              animationDuration: `${3 + Math.random() * 3}s`,
              clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
            }}
          />
        ))}

        {/* Floating Particles */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-white/20 rounded-full animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`,
            }}
          />
        ))}

        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
            backgroundSize: '30px 30px'
          }}></div>
        </div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="flex items-center justify-between h-20">
          {/* Enhanced Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-gray-500 to-gray-600 rounded-xl flex items-center justify-center">
              <Sparkles className="text-white" size={24} />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Sameer Krishn
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.name}
                onClick={() => scrollToSection(item.href)}
                className={`relative px-4 py-2 text-sm font-medium transition-all duration-300 hover:text-white ${activeSection === item.href.substring(1)
                    ? 'text-white'
                    : 'text-gray-400'
                  }`}
              >
                {item.name}
                {activeSection === item.href.substring(1) && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-gray-500 to-gray-600 rounded-full"></div>
                )}
              </button>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 text-gray-400 hover:text-white transition-colors duration-300"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Enhanced Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-full left-0 right-0 bg-gray-900/95 backdrop-blur-xl border-t border-gray-700/50 shadow-2xl">
            <div className="px-4 py-6 space-y-4">
              {navItems.map((item) => (
                <button
                  key={item.name}
                  onClick={() => scrollToSection(item.href)}
                  className={`block w-full text-left px-4 py-3 rounded-xl font-medium transition-all duration-300 hover:scale-105 ${activeSection === item.href.substring(1)
                      ? 'text-white bg-gradient-to-r from-gray-500/20 to-gray-600/20'
                      : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
                    }`}
                >
                  {item.name}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-10px) rotate(180deg); }
        }
        @keyframes cube-float {
          0%, 100% { 
            transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) translateY(0px); 
          }
          25% { 
            transform: rotateX(90deg) rotateY(45deg) rotateZ(0deg) translateY(-10px); 
          }
          50% { 
            transform: rotateX(180deg) rotateY(90deg) rotateZ(45deg) translateY(0px); 
          }
          75% { 
            transform: rotateX(270deg) rotateY(135deg) rotateZ(90deg) translateY(-5px); 
          }
        }
        @keyframes geometric-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          33% { transform: rotateX(120deg) rotateY(120deg) rotateZ(0deg) scale(1.1); }
          66% { transform: rotateX(240deg) rotateY(240deg) rotateZ(120deg) scale(0.9); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(240deg) scale(1); }
        }
        .animate-float {
          animation: float 4s ease-in-out infinite;
        }
        .animate-cube-float {
          animation: cube-float linear infinite;
        }
        .animate-geometric-spin {
          animation: geometric-spin linear infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
      `}</style>
    </header>
  );
};

export default Header;