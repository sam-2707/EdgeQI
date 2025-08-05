import React from 'react';
import { Mail, Phone, MapPin, Github, Linkedin, Sparkles, Send, MessageCircle, CheckCircle } from 'lucide-react';

const Contact = () => {
  const contactInfo = [
    {
      icon: <Mail className="text-gray-300" size={24} />,
      title: "Email",
      value: "krishnsameer54@gmail.com",
      link: "mailto:krishnsameer54@gmail.com"
    },
    {
      icon: <Phone className="text-gray-300" size={24} />,
      title: "Phone",
      value: "+91 630-123-4567",
      link: "tel:+916301234567"
    },
    {
      icon: <MapPin className="text-gray-300" size={24} />,
      title: "Location",
      value: "Hyderabad, India",
      link: "#"
    }
  ];

  const socialLinks = [
    {
      icon: <Github size={24} />,
      href: "https://github.com/sam-2707",
      label: "GitHub"
    },
    {
      icon: <Linkedin size={24} />,
      href: "www.linkedin.com/in/sameer-krishn",
      label: "LinkedIn"
    }
  ];

  return (
    <section id="contact" className="py-24 bg-gradient-to-br from-black via-gray-900 to-black relative overflow-hidden">
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

        {/* 3D Particle Field */}
        {[...Array(25)].map((_, i) => (
          <div
            key={`particle-${i}`}
            className="absolute w-1 h-1 bg-white/30 rounded-full transform-gpu animate-particle-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${4 + Math.random() * 6}s`,
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
              <span className="text-gray-400 font-semibold text-sm uppercase tracking-wider">Get In Touch</span>
              <Sparkles className="text-gray-400 animate-pulse" size={24} />
            </div>
            <h2 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
              Contact Me
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              Let's discuss your next project or just say hello. I'm always open to new opportunities and collaborations.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-16">
            {/* Left Column - Contact Info */}
            <div className="space-y-8">
              {/* Enhanced Contact Info Cards */}
              <div className="space-y-6">
                {contactInfo.map((info, index) => (
                  <a
                    key={index}
                    href={info.link}
                    className="group flex items-center space-x-4 p-6 bg-gray-900/80 backdrop-blur-xl rounded-2xl border border-gray-700/50 hover:border-gray-500/50 transition-all duration-500 hover:scale-105 hover:shadow-2xl"
                  >
                    <div className="flex-shrink-0 p-4 bg-gradient-to-br from-gray-500/20 to-gray-600/20 rounded-xl group-hover:scale-110 transition-transform duration-300">
                      {info.icon}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-1">{info.title}</h3>
                      <p className="text-gray-300 group-hover:text-white transition-colors duration-300">{info.value}</p>
                    </div>
                  </a>
                ))}
              </div>

              {/* Enhanced Social Links */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-6 flex items-center space-x-2">
                  <MessageCircle className="text-gray-400" size={24} />
                  <span>Connect With Me</span>
                </h3>
                <div className="flex space-x-4">
                  {socialLinks.map((social, index) => (
                    <a
                      key={index}
                      href={social.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-4 bg-gray-900/80 backdrop-blur-xl rounded-xl hover:bg-gray-800 transition-all duration-300 group hover:scale-110 hover:shadow-2xl border border-gray-700/50 hover:border-gray-500/50"
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

            {/* Right Column - Contact Form */}
            <div className="bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-700/50 hover:border-gray-500/50 transition-all duration-500">
              <form className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-gray-300 font-medium mb-2">Name</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-gray-500/50 focus:ring-2 focus:ring-gray-500/20 transition-all duration-300"
                      placeholder="Your name"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-gray-300 font-medium mb-2">Email</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-gray-500/50 focus:ring-2 focus:ring-gray-500/20 transition-all duration-300"
                      placeholder="your.email@example.com"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="subject" className="block text-gray-300 font-medium mb-2">Subject</label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-gray-500/50 focus:ring-2 focus:ring-gray-500/20 transition-all duration-300"
                    placeholder="What's this about?"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="message" className="block text-gray-300 font-medium mb-2">Message</label>
                  <textarea
                    id="message"
                    name="message"
                    rows={6}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-600/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-gray-500/50 focus:ring-2 focus:ring-gray-500/20 transition-all duration-300 resize-none"
                    placeholder="Tell me about your project or just say hello..."
                    required
                  ></textarea>
                </div>
                <button
                  type="submit"
                  className="w-full px-8 py-4 bg-gradient-to-r from-gray-700 to-gray-800 text-white font-semibold rounded-xl hover:from-gray-600 hover:to-gray-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center justify-center space-x-2 group"
                >
                  <Send size={20} className="group-hover:animate-pulse" />
                  <span>Send Message</span>
                </button>
              </form>

              {/* Success Message Placeholder */}
              <div className="hidden mt-6 p-4 bg-green-900/20 border border-green-500/30 rounded-xl">
                <div className="flex items-center space-x-2 text-green-400">
                  <CheckCircle size={20} />
                  <span>Message sent successfully!</span>
                </div>
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
        @keyframes icosahedron-spin {
          0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); }
          50% { transform: rotateX(180deg) rotateY(180deg) rotateZ(90deg) scale(1.1); }
          100% { transform: rotateX(360deg) rotateY(360deg) rotateZ(180deg) scale(1); }
        }
        @keyframes tetrahedron-float {
          0%, 100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
          50% { transform: translateY(-25px) rotateX(180deg) rotateY(90deg) rotateZ(90deg); }
        }
        @keyframes particle-float {
          0%, 100% { transform: translateY(0px) translateX(0px) scale(1); }
          25% { transform: translateY(-15px) translateX(10px) scale(1.2); }
          50% { transform: translateY(-30px) translateX(-5px) scale(0.8); }
          75% { transform: translateY(-10px) translateX(-15px) scale(1.1); }
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
        .animate-particle-float {
          animation: particle-float ease-in-out infinite;
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

export default Contact;