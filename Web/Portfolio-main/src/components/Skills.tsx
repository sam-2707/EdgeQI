import React, { useState } from 'react';
import { BrainCircuit, BarChart3, Cpu, Check, Globe, Code, Languages, Sparkles, Zap, Target } from 'lucide-react';

const Skills = () => {
  const [hoveredCategory, setHoveredCategory] = useState<number | null>(null);

  const skillCategories = [
    {
      title: "AI/ML",
      icon: <BrainCircuit className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "TensorFlow / PyTorch",
        "Scikit-learn / XGBoost",
        "Deep Learning (CNN/RNN)",
        "Reinforcement Learning",
      ]
    },
    {
      title: "Data Science",
      icon: <BarChart3 className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "Pandas / NumPy",
        "Matplotlib / Seaborn / Plotly",
        "Data Cleaning & Feature Engg",
        "Model Evaluation / Tuning",
      ]
    },
    {
      title: "Core Electronics",
      icon: <Cpu className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "Verilog / VHDL",
        "Embedded C / C++",
        "Internet of Things / Embedded Systems",
        "Signal Processing (MATLAB)",
      ]
    },
    {
      title: "Fullstack Development",
      icon: <Code className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "React / Next.js / TypeScript",
        "Node.js / Express / MongoDB",
        "Python / Django / Flask",
        "HTML / CSS / JavaScript",
      ]
    },
    {
      title: "Applications",
      icon: <Globe className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "Git / GitHub / GitLab",
        "Docker / Kubernetes",
        "AWS / Azure / GCP",
        "PostgreSQL / MySQL",
      ]
    },
    {
      title: "Speaking Languages",
      icon: <Languages className="text-gray-300" size={32} />,
      gradient: "from-gray-500/20 to-gray-600/20",
      borderGradient: "from-gray-500/50 to-gray-600/50",
      skills: [
        "English (Fluent)",
        "Telugu (Native)",
        "Hindi (Intermediate)",
        "Kannada (Intermediate)",
      ]
    },
  ];

  return (
    <section id="skills" className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-gray-500/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-gray-400/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-gray-600/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>

        {/* 3D Floating Octahedrons */}
        {[...Array(6)].map((_, i) => (
          <div
            key={`octa-${i}`}
            className="absolute w-16 h-16 bg-gradient-to-br from-gray-300/20 to-gray-500/20 transform-gpu animate-octahedron-rotate"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)'
            }}
          />
        ))}

        {/* 3D Dodecahedrons */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`dodeca-${i}`}
            className="absolute w-20 h-20 bg-gradient-to-br from-gray-400/15 to-gray-600/15 transform-gpu animate-dodecahedron-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${8 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 80% 10%, 100% 35%, 100% 70%, 80% 90%, 50% 100%, 20% 90%, 0% 70%, 0% 35%, 20% 10%)'
            }}
          />
        ))}

        {/* 3D Torus Shapes */}
        {[...Array(5)].map((_, i) => (
          <div
            key={`torus-${i}`}
            className="absolute w-12 h-12 border-2 border-gray-400/30 rounded-full transform-gpu animate-torus-rotate"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${4 + Math.random() * 3}s`
            }}
          >
            <div className="w-6 h-6 border border-gray-400/20 rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-inner-torus"></div>
          </div>
        ))}

        {/* Floating Particles */}
        {[...Array(20)].map((_, i) => (
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
              <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">Skills & Expertise</span>
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
            </div>
            <h2 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
              My Skills
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              A comprehensive collection of technologies, tools, and languages I use to bring innovative ideas to life
            </p>
          </div>

          {/* Enhanced Skills Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {skillCategories.map((category, categoryIndex) => (
              <div
                key={categoryIndex}
                className={`relative group cursor-pointer transition-all duration-700 hover:scale-105 hover:-translate-y-2`}
                onMouseEnter={() => setHoveredCategory(categoryIndex)}
                onMouseLeave={() => setHoveredCategory(null)}
              >
                {/* Card Background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${category.gradient} rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>

                {/* Main Card */}
                <div className={`relative bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-700/50 group-hover:border-transparent transition-all duration-700 overflow-hidden`}>
                  {/* Animated Border */}
                  <div className={`absolute inset-0 bg-gradient-to-r ${category.borderGradient} rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>
                  <div className="absolute inset-[2px] bg-gray-900/80 rounded-3xl"></div>

                  {/* Content */}
                  <div className="relative z-10">
                    {/* Icon Container */}
                    <div className="text-center mb-8">
                      <div className={`inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br ${category.gradient} rounded-3xl mb-6 group-hover:scale-110 transition-all duration-500 shadow-2xl`}>
                        <div className="text-white">
                          {category.icon}
                        </div>
                      </div>
                      <h3 className="text-2xl font-bold text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-300 group-hover:bg-clip-text transition-all duration-500">
                        {category.title}
                      </h3>
                    </div>

                    {/* Skills List */}
                    <div className="space-y-4">
                      {category.skills.map((skill, skillIndex) => (
                        <div
                          key={skillIndex}
                          className="flex items-center space-x-4 group/skill hover:bg-white/5 rounded-xl p-3 transition-all duration-300"
                        >
                          <div className="flex-shrink-0 w-6 h-6 bg-gradient-to-br from-gray-500 to-gray-600 rounded-full flex items-center justify-center shadow-lg">
                            <Check className="w-3 h-3 text-white" />
                          </div>
                          <span className="text-gray-300 group-hover/skill:text-white transition-colors duration-300 font-medium">
                            {skill}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Enhanced Status Section */}
          <div className="text-center">
            <div className="inline-flex items-center space-x-4 bg-gradient-to-r from-gray-500/20 to-gray-600/20 backdrop-blur-xl rounded-full px-8 py-4 border border-gray-600/30 hover:border-gray-500/50 transition-all duration-500 hover:scale-105 group">
              <div className="flex items-center space-x-2">
                <Zap className="text-gray-400 animate-pulse" size={20} />
                <Target className="text-gray-400 animate-pulse" size={20} />
              </div>
              <span className="text-gray-200 font-medium">Continuously expanding my skill set</span>
              <div className="flex items-center space-x-2">
                <Target className="text-gray-400 animate-pulse" size={20} />
                <Zap className="text-gray-400 animate-pulse" size={20} />
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
        @keyframes octahedron-rotate {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          50% { transform: rotateX(180deg) rotateY(180deg) rotateZ(90deg) scale(1.2); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(180deg) scale(1); }
        }
        @keyframes dodecahedron-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          100% { transform: rotateX(360deg) rotateY(720deg) rotateZ(360deg); }
        }
        @keyframes torus-rotate {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(720deg); }
        }
        @keyframes inner-torus {
          0% { transform: translate(-50%, -50%) rotateZ(0deg); }
          100% { transform: translate(-50%, -50%) rotateZ(-720deg); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-octahedron-rotate {
          animation: octahedron-rotate linear infinite;
        }
        .animate-dodecahedron-spin {
          animation: dodecahedron-spin linear infinite;
        }
        .animate-torus-rotate {
          animation: torus-rotate linear infinite;
        }
        .animate-inner-torus {
          animation: inner-torus linear infinite;
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

export default Skills;