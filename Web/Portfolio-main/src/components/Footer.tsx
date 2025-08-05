import React from 'react';
import { Github, Linkedin, Mail, Sparkles, Heart } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const quickLinks = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Skills', href: '#skills' },
    { name: 'Projects', href: '#projects' },
    { name: 'Contact', href: '#contact' }
  ];

  const socialLinks = [
    {
      icon: <Github size={20} />,
      href: 'https://github.com/sam-2707',
      label: 'GitHub'
    },
    {
      icon: <Linkedin size={20} />,
      href: 'www.linkedin.com/in/sameer-krishn',
      label: 'LinkedIn'
    },
    {
      icon: <Mail size={20} />,
      href: 'mailto:krishnsameer54@gmail.com',
      label: 'Email'
    }
  ];

  return (
    <footer className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-gray-500/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-gray-400/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-gray-600/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>

        {/* 3D Floating Cubes */}
        {[...Array(6)].map((_, i) => (
          <div
            key={`cube-${i}`}
            className="absolute w-12 h-12 bg-gradient-to-br from-gray-300/15 to-gray-500/15 transform-gpu animate-cube-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
              transform: `rotateX(${Math.random() * 360}deg) rotateY(${Math.random() * 360}deg) rotateZ(${Math.random() * 360}deg)`
            }}
          />
        ))}

        {/* 3D Spheres */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`sphere-${i}`}
            className="absolute w-16 h-16 rounded-full bg-gradient-to-br from-gray-400/20 to-gray-600/20 transform-gpu animate-sphere-bounce"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 4}s`,
              animationDuration: `${3 + Math.random() * 3}s`,
            }}
          />
        ))}

        {/* 3D Rings */}
        {[...Array(5)].map((_, i) => (
          <div
            key={`ring-${i}`}
            className="absolute w-20 h-20 border border-gray-400/20 rounded-full transform-gpu animate-ring-rotate"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${4 + Math.random() * 3}s`
            }}
          >
            <div className="w-12 h-12 border border-gray-400/15 rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-inner-ring"></div>
          </div>
        ))}

        {/* Floating Particles */}
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-white/30 rounded-full animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${3 + Math.random() * 4}s`,
            }}
          />
        ))}

        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
            backgroundSize: '50px 50px'
          }}></div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16 relative z-10">
        <div className="max-w-7xl mx-auto">
          {/* Enhanced Footer Content */}
          <div className="grid md:grid-cols-3 gap-12 mb-12">
            {/* Logo and Description */}
            <div className="space-y-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-gray-500 to-gray-600 rounded-xl flex items-center justify-center">
                  <Sparkles className="text-white" size={24} />
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Sameer Krishn
                </span>
              </div>
              <p className="text-gray-400 leading-relaxed max-w-md">
                AI/ML Engineer passionate about creating intelligent solutions and pushing the boundaries of technology.
                Building the future, one algorithm at a time.
              </p>
            </div>

            {/* Quick Links */}
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-white mb-4">Quick Links</h3>
              <div className="space-y-3">
                {quickLinks.map((link, index) => (
                  <a
                    key={index}
                    href={link.href}
                    className="block text-gray-400 hover:text-white transition-colors duration-300 hover:scale-105 transform"
                  >
                    {link.name}
                  </a>
                ))}
              </div>
            </div>

            {/* Social Links */}
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-white mb-4">Connect</h3>
              <div className="flex space-x-4">
                {socialLinks.map((social, index) => (
                  <a
                    key={index}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-3 bg-gray-900/80 backdrop-blur-xl rounded-xl hover:bg-gray-800 transition-all duration-300 group hover:scale-110 hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
                    aria-label={social.label}
                  >
                    <div className="text-gray-300 group-hover:text-white transition-colors duration-300">
                      {social.icon}
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Enhanced Bottom Section */}
          <div className="border-t border-gray-800 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <div className="text-gray-400 text-sm">
                © {currentYear} Sameer Krishn. All rights reserved.
              </div>

              <div className="flex items-center space-x-6 text-sm">
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Privacy Policy
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Terms of Service
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Cookie Policy
                </a>
              </div>
            </div>

            {/* Enhanced Crafted With Love */}
            <div className="text-center mt-8">
              <div className="inline-flex items-center space-x-2 px-6 py-3 bg-gray-900/50 backdrop-blur-xl rounded-full border border-gray-700/50">
                <span className="text-gray-400 text-sm">Crafted with</span>
                <Heart className="text-gray-400 animate-pulse" size={16} />
                <span className="text-gray-400 text-sm">by Sameer Krishn</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        @keyframes cube-float {
          0%, 100% { 
            transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) translateY(0px); 
          }
          25% { 
            transform: rotateX(90deg) rotateY(45deg) rotateZ(0deg) translateY(-20px); 
          }
          50% { 
            transform: rotateX(180deg) rotateY(90deg) rotateZ(45deg) translateY(0px); 
          }
          75% { 
            transform: rotateX(270deg) rotateY(135deg) rotateZ(90deg) translateY(-10px); 
          }
        }
        @keyframes sphere-bounce {
          0%, 100% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(-30px) scale(1.1); }
        }
        @keyframes ring-rotate {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          100% { transform: rotateX(360deg) rotateY(180deg) rotateZ(360deg); }
        }
        @keyframes inner-ring {
          0% { transform: translate(-50%, -50%) rotateZ(0deg); }
          100% { transform: translate(-50%, -50%) rotateZ(-360deg); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-cube-float {
          animation: cube-float linear infinite;
        }
        .animate-sphere-bounce {
          animation: sphere-bounce ease-in-out infinite;
        }
        .animate-ring-rotate {
          animation: ring-rotate linear infinite;
        }
        .animate-inner-ring {
          animation: inner-ring linear infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </footer>
  );
};

export default Footer;