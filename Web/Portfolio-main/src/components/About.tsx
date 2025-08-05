import React from 'react';
import { BrainCircuit, BarChart3, Cpu, Sparkles, User } from 'lucide-react';
import myPhoto from '../assets/myphoto.jpg';

const About = () => {
  const highlights = [
    {
      icon: <BrainCircuit className="text-gray-300" size={24} />,
      title: "AI & Machine Learning",
      description: "Building intelligent systems with deep learning, transformers, and reinforcement learning.",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      icon: <BarChart3 className="text-gray-300" size={24} />,
      title: "Data Science",
      description: "Extracting insights with data analysis, visualization, and advanced model tuning.",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      icon: <Cpu className="text-gray-300" size={24} />,
      title: "Core Electronics",
      description: "Designing embedded systems, signal processing, and PCB development.",
      gradient: "from-gray-500/20 to-gray-600/20"
    }
  ];

  return (
    <section id="about" className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-gray-500/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-gray-400/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-gray-600/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>

        {/* 3D Floating Diamonds */}
        {[...Array(8)].map((_, i) => (
          <div
            key={`diamond-${i}`}
            className="absolute w-12 h-12 bg-gradient-to-br from-gray-300/20 to-gray-500/20 transform-gpu animate-diamond-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)'
            }}
          />
        ))}

        {/* 3D Hexagons */}
        {[...Array(6)].map((_, i) => (
          <div
            key={`hex-${i}`}
            className="absolute w-16 h-16 bg-gradient-to-br from-gray-300/15 to-gray-500/15 transform-gpu animate-hexagon-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${4 + Math.random() * 4}s`,
              clipPath: 'polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%)'
            }}
          />
        ))}

        {/* 3D Pyramids */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`pyramid-${i}`}
            className="absolute w-20 h-20 bg-gradient-to-br from-gray-400/20 to-gray-600/20 transform-gpu animate-pyramid-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${5 + Math.random() * 3}s`,
              clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
            }}
          />
        ))}

        {/* Floating Particles */}
        {[...Array(12)].map((_, i) => (
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

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-7xl mx-auto">
          {/* Enhanced Section Header */}
          <div className="text-center mb-20">
            <div className="inline-flex items-center space-x-2 mb-6">
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
              <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">About Me</span>
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
            </div>
            <h2 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
              About Me
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              Passionate about creating digital experiences that push the boundaries of what's possible
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-16 items-center">
            {/* Left Column - Enhanced Avatar */}
            <div className="relative">
              <div className="relative z-10">
                <div className="w-full max-w-md mx-auto aspect-square rounded-3xl bg-gradient-to-br from-gray-500/20 to-gray-600/20 p-8 flex items-center justify-center hover:scale-105 transition-all duration-500 group shadow-2xl">
                  <img
                    src={myPhoto}
                    alt="Sameer Krishn"
                    className="rounded-2xl w-full h-full object-cover group-hover:scale-110 transition-all duration-500"
                  />
                </div>
              </div>
              <div className="absolute -top-6 -right-6 w-full h-full rounded-3xl bg-gradient-to-br from-gray-500/30 to-gray-600/30 -z-10 blur-xl"></div>
            </div>

            {/* Right Column - Content */}
            <div className="space-y-8">
              <div className="space-y-6">
                <div className="flex items-center space-x-3 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-gray-500 to-gray-600 rounded-xl flex items-center justify-center">
                    <User className="text-white" size={24} />
                  </div>
                  <h3 className="text-3xl font-bold text-white">Hi there! I'm Sameer Krishn</h3>
                </div>
                <p className="text-gray-300 leading-relaxed text-lg">
                  A versatile developer blending AI/ML, data science, full-stack engineering, and hardware design to build smart, interactive, and future-ready applications. With hands-on expertise across deep learning, embedded systems, and modern web technologies, I create solutions that are both intelligent and visually compelling.
                </p>
                <p className="text-gray-300 leading-relaxed text-lg">
                  When I'm not training models or crafting immersive 3D interfaces, you'll find me experimenting with microcontrollers, optimizing machine learning workflows, or contributing to projects that bridge hardware, software, and design.
                </p>
              </div>

              {/* Enhanced Highlights */}
              <div className="grid gap-6 mt-8">
                {highlights.map((item, index) => (
                  <div key={index} className={`flex items-start space-x-4 p-6 bg-gray-900/80 backdrop-blur-xl rounded-xl border border-gray-700/50 hover:border-transparent transition-all duration-500 group hover:scale-105 hover:shadow-2xl`}>
                    {/* Animated Border */}
                    <div className={`absolute inset-0 bg-gradient-to-r ${item.gradient} rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500`}></div>
                    <div className="absolute inset-[2px] bg-gray-900/80 rounded-xl"></div>

                    {/* Content */}
                    <div className="relative z-10 flex items-start space-x-4">
                      <div className="flex-shrink-0 p-3 bg-gradient-to-br from-gray-500/20 to-gray-600/20 rounded-xl group-hover:scale-110 transition-transform duration-300">
                        {item.icon}
                      </div>
                      <div>
                        <h4 className="font-semibold text-white mb-2 text-lg">{item.title}</h4>
                        <p className="text-gray-400 leading-relaxed">{item.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
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
        @keyframes diamond-spin {
          0% { transform: rotateZ(0deg) rotateX(0deg) rotateY(0deg); }
          100% { transform: rotateZ(360deg) rotateX(180deg) rotateY(360deg); }
        }
        @keyframes hexagon-float {
          0%, 100% { transform: translateY(0px) rotateZ(0deg); }
          50% { transform: translateY(-20px) rotateZ(180deg); }
        }
        @keyframes pyramid-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          50% { transform: rotateX(180deg) rotateY(180deg) rotateZ(90deg) scale(1.2); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(180deg) scale(1); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-diamond-spin {
          animation: diamond-spin linear infinite;
        }
        .animate-hexagon-float {
          animation: hexagon-float ease-in-out infinite;
        }
        .animate-pyramid-spin {
          animation: pyramid-spin linear infinite;
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

export default About;