import React from 'react';
import { Sparkles, ExternalLink, Github, Calendar } from 'lucide-react';

const Projects = () => {
  const projects = [
    {
      title: "Pothole Detection and Smart Navigation System",
      description: "An intelligent system that detects potholes in road images using deep learning and dynamically reroutes vehicles around them with smart path planning.",
      image: "https://i.dailymail.co.uk/1s/2021/12/09/20/51566381-0-image-a-8_1639081829906.jpg",
      tech: ["Python", "TensorFlow", "Keras", "OpenCV", "Deep Learning", "Computer Vision"],
      github: "https://github.com/sam-2707/Pothole_Detecor",
      live: "https://github.com/sam-2707/Pothole_Detecor",
      date: "Jan 2025 - Present",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      title: "Type 2 Diabetes Mellitus Prediction using Advanced Algorithms",
      description: "A machine learning model that predicts the likelihood of Type 2 Diabetes Mellitus using advanced algorithms and machine learning techniques.",
      image: "https://eco-intelligent.com/wp-content/uploads/2020/09/genes.jpg?w=900",
      tech: ["Python", "TensorFlow", "Keras", "Machine Learning", "Advanced Algorithms"],
      github: "https://github.com/sam-2707/Diabetes-Prediction-Model",
      live: "https://github.com/sam-2707/Diabetes-Prediction-Model",
      date: "August 2024 - Present",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      title: "Processing Element for DOA Estimation",
      description: "A hardware-accelerated Processing Element (PE) designed for efficient Direction-of-Arrival (DOA) estimation using OMP, featuring complex arithmetic and optimized parallel computation on FPGA.",
      image: "https://static.vecteezy.com/system/resources/previews/024/397/262/non_2x/central-processing-unit-icon-design-microchip-sign-and-symbol-computer-element-illustration-vector.jpg",
      tech: ["Xilinx", "Vivado", "Verilog", "FPGA", "Hardware Design"],
      github: "https://github.com/sam-2707/Processing-Element-for-DOA",
      live: "https://github.com/sam-2707/Processing-Element-for-DOA",
      date: "February 2025 - March 2025",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      title: "Gaming Tournament Registration System",
      description: "A dynamic website showcasing 'GG' — a gaming event featuring tournaments like Valorant, FIFA, BGMI, Free Fire, a VR/AR hackathon, and an immersive console gaming arena.",
      image: "https://cdn.bluent.com/images/wher-are-we-going.webp",
      tech: ["Vite.js", "Tailwind CSS", "React", "Node.js", "Express.js", "MongoDB", "Firebase"],
      github: "https://github.com/sam-2707/forge-main",
      live: "https://forge-main.vercel.app",
      date: "2023",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      title: "5G + LiFi Integration",
      description: "This project focuses on accessing and analyzing digital I/Q signals from the USRP B210 before analog conversion. It involves understanding the SDR architecture, especially the AD9361 transceiver's digital-to-analog pathway.",
      image: "https://www.iberdrola.com/documents/20125/40459/lifi_nueva_746x419.jpg/8d21970e-8f8f-514c-060c-825440dff749?t=1627370903097",
      tech: ["USRP B210", "SDR", "Signal Processing", "Digital Signal Processing", "Radio Frequency"],
      github: "https://github.com/sam-2707/5G-LiFi-Integration",
      live: "https://github.com/sam-2707/5G-LiFi-Integration",
      date: "Working on it",
      gradient: "from-gray-500/20 to-gray-600/20"
    },
    {
      title: "QFLARE",
      description: "QFLARE integrates Federated Learning (FL) with a robust, multi-layered security architecture. At its core, the system uses a Post-Quantum Cryptography (PQC) suite for all communication, combining a Key Encapsulation Mechanism (KEM) with digital signatures to ensure confidentiality, integrity, and authentication. ",
      image: "https://making-pictures.com/wp-content/uploads/2023/12/jamie-jones-IBM-Quantum_Hero_layer-file-1.jpg",
      tech: ["Quantum Computing", "Quantum Cryptography", "Quantum Key Distribution", "Quantum Machine Learning", "Quantum Networking"],
      github: "https://github.com/sam-2707/QFLARE",
      live: "#https://github.com/sam-2707/QFLARE",
      date: "Working on it",
      gradient: "from-gray-500/20 to-gray-600/20"
    }
  ];

  return (
    <section id="projects" className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
      {/* Enhanced Background Elements */}
      <div className="absolute inset-0">
        {/* Animated Gradient Orbs */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-gray-500/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-gray-400/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-gray-600/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>

        {/* 3D Floating Icosahedrons */}
        {[...Array(6)].map((_, i) => (
          <div
            key={`icosa-${i}`}
            className="absolute w-20 h-20 bg-gradient-to-br from-gray-300/20 to-gray-500/20 transform-gpu animate-icosahedron-spin"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${8 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 80% 10%, 100% 35%, 100% 70%, 80% 90%, 50% 100%, 20% 90%, 0% 70%, 0% 35%, 20% 10%)'
            }}
          />
        ))}

        {/* 3D Tetrahedrons */}
        {[...Array(8)].map((_, i) => (
          <div
            key={`tetra-${i}`}
            className="absolute w-16 h-16 bg-gradient-to-br from-gray-400/15 to-gray-600/15 transform-gpu animate-tetrahedron-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
              clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
            }}
          />
        ))}

        {/* 3D Wireframe Grid */}
        {[...Array(4)].map((_, i) => (
          <div
            key={`grid-${i}`}
            className="absolute w-24 h-24 border border-gray-400/20 transform-gpu animate-grid-rotate"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${5 + Math.random() * 3}s`
            }}
          >
            <div className="w-full h-full border border-gray-400/20"></div>
            <div className="w-full h-full border border-gray-400/20 transform rotate-45"></div>
          </div>
        ))}

        {/* Floating Particles */}
        {[...Array(18)].map((_, i) => (
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
              <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">Featured Work</span>
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
            </div>
            <h2 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
              My Projects
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              A showcase of my technical expertise across AI/ML, embedded systems, and full-stack development
            </p>
          </div>

          {/* Enhanced Projects Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {projects.map((project, index) => (
              <div
                key={index}
                className="group relative cursor-pointer transition-all duration-700 hover:scale-105 hover:-translate-y-2"
              >
                {/* Card Background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${project.gradient} rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>

                {/* Main Card */}
                <div className="relative bg-gray-900/80 backdrop-blur-xl rounded-3xl overflow-hidden border border-gray-700/50 group-hover:border-transparent transition-all duration-700">
                  {/* Animated Border */}
                  <div className={`absolute inset-0 bg-gradient-to-r ${project.gradient} rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>
                  <div className="absolute inset-[2px] bg-gray-900/80 rounded-3xl"></div>

                  {/* Content */}
                  <div className="relative z-10">
                    {/* Project Image */}
                    <div className="relative overflow-hidden">
                      <img
                        src={project.image}
                        alt={project.title}
                        className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-110"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-gray-900/80 to-transparent group-hover:from-gray-900/60 transition-all duration-300"></div>

                      {/* Date Badge */}
                      <div className="absolute top-4 right-4 flex items-center space-x-1 bg-gray-900/80 rounded-full px-3 py-1 backdrop-blur-sm">
                        <Calendar size={14} className="text-gray-400" />
                        <span className="text-sm text-gray-400">{project.date}</span>
                      </div>

                      {/* Hover Overlay */}
                      <div className="absolute inset-0 bg-gradient-to-br from-gray-600/20 to-gray-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                        <div className="flex space-x-4">
                          <a
                            href={project.github}
                            className="p-4 bg-gray-900/80 rounded-xl hover:bg-gray-800 transition-colors transform hover:scale-110 shadow-2xl backdrop-blur-sm"
                          >
                            <Github size={24} className="text-white" />
                          </a>
                          <a
                            href={project.live}
                            className="p-4 bg-gray-600/80 rounded-xl hover:bg-gray-700 transition-colors transform hover:scale-110 shadow-2xl backdrop-blur-sm"
                          >
                            <ExternalLink size={24} className="text-white" />
                          </a>
                        </div>
                      </div>
                    </div>

                    {/* Project Content */}
                    <div className="p-6">
                      <h3 className="text-xl font-bold text-white mb-3 group-hover:text-gray-400 transition-colors duration-300">
                        {project.title}
                      </h3>
                      <p className="text-gray-400 text-sm mb-4 leading-relaxed">
                        {project.description}
                      </p>

                      {/* Tech Stack */}
                      <div className="flex flex-wrap gap-2 mb-6">
                        {project.tech.map((tech, techIndex) => (
                          <span
                            key={techIndex}
                            className="px-3 py-1 bg-gray-800 text-gray-300 text-xs rounded-full border border-gray-700 hover:border-gray-500/50 hover:text-white transition-all duration-300 hover:scale-105"
                          >
                            {tech}
                          </span>
                        ))}
                      </div>

                      {/* Project Links */}
                      <div className="flex space-x-4">
                        <a
                          href={project.github}
                          className="flex items-center space-x-2 text-gray-300 hover:text-white transition-all duration-300 hover:scale-105"
                        >
                          <Github size={16} />
                          <span className="text-sm">Code</span>
                        </a>
                        <a
                          href={project.live}
                          className="flex items-center space-x-2 text-gray-300 hover:text-white transition-all duration-300 hover:scale-105"
                        >
                          <ExternalLink size={16} />
                          <span className="text-sm">Live Demo</span>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Enhanced View More Button */}
          <div className="text-center mt-16">
            <a
              href="https://github.com/sam-2707"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center space-x-2 px-10 py-4 bg-gradient-to-r from-gray-600 to-gray-700 text-white font-semibold rounded-xl hover:from-gray-500 hover:to-gray-600 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl relative overflow-hidden group"
            >
              <span className="relative z-10 flex items-center justify-center space-x-2">
                <ExternalLink size={18} className="group-hover:animate-pulse" />
                <span>Explore More Projects</span>
              </span>
            </a>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        @keyframes icosahedron-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          50% { transform: rotateX(180deg) rotateY(180deg) rotateZ(90deg) scale(1.1); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(180deg) scale(1); }
        }
        @keyframes tetrahedron-float {
          0%, 100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          50% { transform: translateY(-25px) rotateX(180deg) rotateY(90deg) rotateZ(90deg); }
        }
        @keyframes grid-rotate {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(360deg); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-icosahedron-spin {
          animation: icosahedron-spin linear infinite;
        }
        .animate-tetrahedron-float {
          animation: tetrahedron-float ease-in-out infinite;
        }
        .animate-grid-rotate {
          animation: grid-rotate linear infinite;
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

export default Projects;