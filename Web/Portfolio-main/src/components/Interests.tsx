import React from 'react';
import { Sparkles, Music, Gamepad2, Film, Utensils, Code, BookOpen, Trophy, Heart } from 'lucide-react';

const Interests = () => {
    const interests = [
        {
            icon: <Trophy className="text-gray-300" size={32} />,
            title: "Sports Lover",
            description: "Bug-chasing cardio enthusiast",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Music className="text-gray-300" size={32} />,
            title: "Melophile",
            description: "Music in my veins",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Gamepad2 className="text-gray-300" size={32} />,
            title: "Gamer",
            description: "Virtual world explorer",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Film className="text-gray-300" size={32} />,
            title: "Cinephile",
            description: "Movie buff extraordinaire",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Utensils className="text-gray-300" size={32} />,
            title: "Foodie",
            description: "Culinary explorer",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Code className="text-gray-300" size={32} />,
            title: "Vibe Coder",
            description: "Bug whisperer & code poet",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <BookOpen className="text-gray-300" size={32} />,
            title: "Poet",
            description: "Wordsmith & verse creator",
            gradient: "from-gray-500/20 to-gray-600/20"
        },
        {
            icon: <Heart className="text-gray-300" size={32} />,
            title: "Life Enthusiast",
            description: "Embracing every moment",
            gradient: "from-gray-500/20 to-gray-600/20"
        }
    ];

    return (
        <section className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
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
                            animationDelay: `${Math.random() * 6}s`,
                            animationDuration: `${4 + Math.random() * 3}s`,
                            clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)'
                        }}
                    />
                ))}

                {/* 3D Floating Hexagons */}
                {[...Array(6)].map((_, i) => (
                    <div
                        key={`hex-${i}`}
                        className="absolute w-16 h-16 bg-gradient-to-br from-gray-400/15 to-gray-600/15 transform-gpu animate-hexagon-float"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                            animationDelay: `${Math.random() * 5}s`,
                            animationDuration: `${5 + Math.random() * 3}s`,
                            clipPath: 'polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%)'
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

            <div className="container mx-auto px-4 relative z-10">
                <div className="max-w-7xl mx-auto">
                    {/* Enhanced Section Header */}
                    <div className="text-center mb-20">
                        <div className="inline-flex items-center space-x-2 mb-6">
                            <Sparkles className="text-gray-400 animate-pulse" size={24} />
                            <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">Beyond Code</span>
                            <Sparkles className="text-gray-400 animate-pulse" size={24} />
                        </div>
                        <h2 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
                            The Many Faces of Me
                        </h2>
                        <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                            When I'm not crafting code, you'll find me exploring life's beautiful moments
                        </p>
                    </div>

                    {/* Enhanced Interests Grid */}
                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
                        {interests.map((interest, index) => (
                            <div
                                key={index}
                                className="group relative cursor-pointer transition-all duration-700 hover:scale-105 hover:-translate-y-2"
                            >
                                {/* Card Background */}
                                <div className={`absolute inset-0 bg-gradient-to-br ${interest.gradient} rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>

                                {/* Main Card */}
                                <div className="relative bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-700/50 group-hover:border-transparent transition-all duration-700 overflow-hidden">
                                    {/* Animated Border */}
                                    <div className={`absolute inset-0 bg-gradient-to-r ${interest.gradient} rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700`}></div>
                                    <div className="absolute inset-[2px] bg-gray-900/80 rounded-3xl"></div>

                                    {/* Content */}
                                    <div className="relative z-10 text-center">
                                        {/* Icon Container */}
                                        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-gray-500/20 to-gray-600/20 rounded-3xl mb-6 group-hover:scale-110 transition-all duration-500 shadow-2xl">
                                            <div className="text-white">
                                                {interest.icon}
                                            </div>
                                        </div>

                                        {/* Title and Description */}
                                        <h3 className="text-xl font-bold text-white mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-300 group-hover:bg-clip-text transition-all duration-500">
                                            {interest.title}
                                        </h3>
                                        <p className="text-gray-400 group-hover:text-gray-300 transition-colors duration-300">
                                            {interest.description}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Enhanced Connect Section */}
                    <div className="text-center">
                        <h3 className="text-3xl font-bold text-white mb-8">
                            Let's Connect & Create Magic ✨
                        </h3>
                        <p className="text-gray-300 text-lg mb-12 max-w-2xl mx-auto">
                            Ready to collaborate on exciting projects or just share a coffee chat about tech, life, and everything in between
                        </p>

                        {/* Social Links */}
                        <div className="flex justify-center space-x-6">
                            <a
                                href="https://github.com/sam-2707"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-4 bg-gradient-to-br from-gray-500/20 to-gray-600/20 backdrop-blur-xl rounded-full hover:scale-110 transition-all duration-300 group hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
                            >
                                <Code size={24} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
                            </a>
                            <a
                                href="www.linkedin.com/in/sameer-krishn"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-4 bg-gradient-to-br from-gray-500/20 to-gray-600/20 backdrop-blur-xl rounded-full hover:scale-110 transition-all duration-300 group hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
                            >
                                <Sparkles size={24} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
                            </a>
                            <a
                                href="mailto:krishnsameer54@gmail.com"
                                className="p-4 bg-gradient-to-br from-gray-500/20 to-gray-600/20 backdrop-blur-xl rounded-full hover:scale-110 transition-all duration-300 group hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
                            >
                                <Heart size={24} className="text-gray-300 group-hover:text-white transition-colors duration-300" />
                            </a>
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
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-diamond-spin {
          animation: diamond-spin linear infinite;
        }
        .animate-hexagon-float {
          animation: hexagon-float ease-in-out infinite;
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

export default Interests; 