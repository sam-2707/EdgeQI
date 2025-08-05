import React from 'react';
import { ArrowDown, Github, Linkedin, Mail, Sparkles, Zap } from 'lucide-react';

const Hero = () => {
  const scrollToAbout = () => {
    const aboutSection = document.getElementById('about');
    if (aboutSection) {
      aboutSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Enhanced Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-gray-500/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-gray-400/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-gray-600/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>

        {/* 3D Floating Cubes */}
        {[...Array(8)].map((_, i) => (
          <div
            key={`cube-${i}`}
            className="absolute w-16 h-16 bg-gradient-to-br from-gray-400/20 to-gray-600/20 transform-gpu animate-cube-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
              transform: `rotateX(${Math.random() * 360}deg) rotateY(${Math.random() * 360}deg) rotateZ(${Math.random() * 360}deg)`
            }}
          />
        ))}

        {/* 3D Geometric Shapes */}
        {[...Array(6)].map((_, i) => (
          <div
            key={`geo-${i}`}
            className="absolute w-20 h-20 bg-gradient-to-br from-gray-300/15 to-gray-500/15 transform-gpu animate-geometric-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${4 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
            }}
          />
        ))}

        {/* 3D Spheres */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`sphere-${i}`}
            className="absolute w-24 h-24 rounded-full bg-gradient-to-br from-gray-400/25 to-gray-600/25 transform-gpu animate-sphere-bounce"
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
            className="absolute w-16 h-16 border-2 border-gray-400/30 rounded-full transform-gpu animate-ring-rotate"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${4 + Math.random() * 3}s`
            }}
          />
        ))}

        {/* Floating Particles */}
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-white/20 rounded-full animate-float"
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

      <div className="container mx-auto px-4 text-center relative z-10">
        <div className="max-w-5xl mx-auto">
          {/* Enhanced Profile Avatar */}
          <div className="mb-12">
            <div className="w-40 h-40 mx-auto rounded-full bg-gradient-to-br from-gray-500 to-gray-600 p-1 hover:scale-110 transition-all duration-500 shadow-2xl">
              <div className="w-full h-full rounded-full bg-gray-900 flex items-center justify-center relative overflow-hidden group">
                <span className="text-5xl font-bold text-white">SK</span>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="mb-8">
            <div className="inline-flex items-center space-x-2 mb-6">
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
              <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">Welcome</span>
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
            </div>

            <h1 className="text-6xl md:text-8xl font-bold mb-6 leading-tight">
              <span className="block text-white mb-2">Hello, I'm</span>
              <span className="block bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
                Sameer Krishn
              </span>
            </h1>

            <p className="text-2xl md:text-3xl text-gray-300 mb-4 font-light">
              AI/ML Engineer
            </p>

            <p className="text-lg text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
              Building smart solutions with machine learning, deep learning, and real-world data.
              Passionate about solving complex problems through code and creativity.
            </p>
          </div>

          {/* Enhanced Social Links */}
          <div className="flex justify-center space-x-6 mb-12">
            <a
              href="https://github.com/sam-2707"
              className="p-4 bg-gray-900/80 backdrop-blur-xl rounded-xl hover:bg-gradient-to-r hover:from-gray-500/20 hover:to-gray-600/20 transition-all duration-300 group hover:scale-110 hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
            >
              <Github size={28} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
            </a>
            <a
              href="www.linkedin.com/in/sameer-krishn"
              className="p-4 bg-gray-900/80 backdrop-blur-xl rounded-xl hover:bg-gradient-to-r hover:from-gray-500/20 hover:to-gray-600/20 transition-all duration-300 group hover:scale-110 hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
            >
              <Linkedin size={28} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
            </a>
            <a
              href="mailto:krishnsameer54@gmail.com"
              className="p-4 bg-gray-900/80 backdrop-blur-xl rounded-xl hover:bg-gradient-to-r hover:from-gray-500/20 hover:to-gray-600/20 transition-all duration-300 group hover:scale-110 hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
            >
              <Mail size={28} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
            </a>
          </div>

          {/* Enhanced CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
            <button
              onClick={scrollToAbout}
              className="px-10 py-4 bg-gradient-to-r from-gray-600 to-gray-700 text-white font-semibold rounded-xl hover:from-gray-500 hover:to-gray-600 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl relative overflow-hidden group"
            >
              <span className="relative z-10 flex items-center justify-center space-x-2">
                <Zap size={18} className="group-hover:animate-pulse" />
                <span>Explore My Work</span>
              </span>
            </button>
            <a
              href="/resume.pdf"
              download
              className="px-10 py-4 border-2 border-gray-600 text-gray-300 font-semibold rounded-xl hover:bg-gradient-to-r hover:from-gray-500/20 hover:to-gray-600/20 hover:text-white hover:border-gray-500 transition-all duration-300 hover:scale-105 hover:shadow-2xl relative overflow-hidden group text-center"
            >
              <span className="relative z-10">Download CV</span>
            </a>
          </div>

          {/* Enhanced Scroll Indicator */}
          <button
            onClick={scrollToAbout}
            className="absolute bottom-8 left-1/2 transform -translate-x-1/2 hover:text-gray-400 transition-colors duration-300 animate-bounce"
          >
            <ArrowDown size={28} className="text-gray-400" />
          </button>
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
        @keyframes geometric-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          33% { transform: rotateX(120deg) rotateY(120deg) rotateZ(0deg) scale(1.1); }
          66% { transform: rotateX(240deg) rotateY(240deg) rotateZ(120deg) scale(0.9); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(240deg) scale(1); }
        }
        @keyframes sphere-bounce {
          0%, 100% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(-30px) scale(1.1); }
        }
        @keyframes ring-rotate {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          100% { transform: rotateX(360deg) rotateY(180deg) rotateZ(360deg); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-cube-float {
          animation: cube-float linear infinite;
        }
        .animate-geometric-spin {
          animation: geometric-spin linear infinite;
        }
        .animate-sphere-bounce {
          animation: sphere-bounce ease-in-out infinite;
        }
        .animate-ring-rotate {
          animation: ring-rotate linear infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </section>
  );
};

export default Hero;