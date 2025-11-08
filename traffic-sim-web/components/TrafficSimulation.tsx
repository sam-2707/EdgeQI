'use client'

import { useRef, useEffect, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Grid, Sky } from '@react-three/drei'
import * as THREE from 'three'
import { useSimulationStore } from '@/store/simulationStore'

// Vehicle Component with Brake Lights
function Vehicle({ position, color, type, isStopped }: { position: [number, number, number], color: string, type: string, isStopped?: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const size: [number, number, number] = type === 'bus' ? [4, 2, 2] : type === 'truck' ? [3.5, 2.5, 2] : [2.5, 1.5, 1.5]
  
  return (
    <group position={position}>
      {/* Vehicle body */}
      <mesh ref={meshRef} castShadow>
        <boxGeometry args={size} />
        <meshStandardMaterial color={color} />
      </mesh>
      
      {/* Brake lights (red when stopped) */}
      {isStopped && (
        <>
          <mesh position={[-size[0]/4, 0, -size[2]/2 - 0.1]}>
            <sphereGeometry args={[0.15, 8, 8]} />
            <meshBasicMaterial color="#ff0000" />
          </mesh>
          <mesh position={[size[0]/4, 0, -size[2]/2 - 0.1]}>
            <sphereGeometry args={[0.15, 8, 8]} />
            <meshBasicMaterial color="#ff0000" />
          </mesh>
          <pointLight position={[0, 0, -size[2]/2 - 0.5]} color="#ff0000" intensity={2} distance={3} />
        </>
      )}
    </group>
  )
}

// Traffic Light Component
function TrafficLight3D({ position, state }: { position: [number, number, number], state: 'red' | 'yellow' | 'green' }) {
  const colors = {
    red: '#ff0000',
    yellow: '#ffff00',
    green: '#00ff00'
  }
  
  return (
    <group position={position}>
      {/* Pole */}
      <mesh position={[0, 0, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.1, 3, 8]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      
      {/* Light housing */}
      <mesh position={[0, 1.5, 0]} castShadow>
        <boxGeometry args={[0.3, 0.8, 0.2]} />
        <meshStandardMaterial color="#222222" />
      </mesh>
      
      {/* Active light */}
      <mesh position={[0, 1.5, 0.15]}>
        <circleGeometry args={[0.12, 16]} />
        <meshBasicMaterial color={colors[state]} />
      </mesh>
      
      {/* Light glow effect */}
      <pointLight
        position={[0, 1.5, 0.3]}
        color={colors[state]}
        intensity={2}
        distance={5}
      />
    </group>
  )
}

// Camera Marker Component
function CameraMarker({ position, name, active }: { position: [number, number, number], name: string, active: boolean }) {
  return (
    <group position={position}>
      {/* Camera body */}
      <mesh castShadow>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshStandardMaterial color={active ? '#00ff00' : '#666666'} emissive={active ? '#00ff00' : '#000000'} emissiveIntensity={0.5} />
      </mesh>
      
      {/* Camera lens */}
      <mesh position={[0, 0, 0.3]} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <cylinderGeometry args={[0.15, 0.15, 0.4, 8]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      
      {/* Active indicator light */}
      {active && (
        <pointLight
          position={[0, 0, 0]}
          color="#00ff00"
          intensity={1}
          distance={3}
        />
      )}
    </group>
  )
}

// Road Intersection Component
function RoadIntersection() {
  return (
    <group>
      {/* Main Roads */}
      {/* North-South road */}
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[8, 40]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      
      {/* East-West road */}
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, Math.PI / 2]} receiveShadow>
        <planeGeometry args={[8, 40]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      
      {/* Center intersection */}
      <mesh position={[0, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[8, 8]} />
        <meshStandardMaterial color="#2a2a2a" />
      </mesh>
      
      {/* Lane markings */}
      {[-10, -5, 5, 10].map((z, i) => (
        <mesh key={`lane-ns-${i}`} position={[0, 0.02, z]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.2, 2]} />
          <meshStandardMaterial color="#ffff00" />
        </mesh>
      ))}
      
      {[-10, -5, 5, 10].map((x, i) => (
        <mesh key={`lane-ew-${i}`} position={[x, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[2, 0.2]} />
          <meshStandardMaterial color="#ffff00" />
        </mesh>
      ))}
      
      {/* Crosswalks */}
      {[[-4, 4], [4, 4], [-4, -4], [4, -4]].map(([x, z], i) => (
        <group key={`crosswalk-${i}`}>
          {Array.from({ length: 5 }).map((_, j) => (
            <mesh key={j} position={[x + (Math.abs(x) === 4 ? j * 0.4 - 0.8 : 0), 0.03, z + (Math.abs(z) === 4 ? j * 0.4 - 0.8 : 0)]} rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[0.3, Math.abs(x) === 4 ? 0.3 : 1, Math.abs(z) === 4 ? 0.3 : 1]} />
              <meshStandardMaterial color="#ffffff" />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  )
}

// Animation Loop Component with Realistic Traffic Logic
function SimulationLoop() {
  const { vehicles, isRunning, addVehicle, updateVehicle, removeVehicle, updateMetrics, updateCamera, updateTrafficLight, trafficLights } = useSimulationStore()
  const frameCount = useRef(0)
  const lastSpawn = useRef(0)
  
  // Helper: Check if vehicle should stop at traffic light
  const shouldStopAtLight = (vehicle: any, lights: any[]) => {
    const { position, direction } = vehicle
    const [x, z] = [position[0], position[2]]
    
    // Larger detection zones for better traffic light obedience
    // Check North-South traffic light (light-ns)
    const nsLight = lights.find(l => l.id === 'light-ns')
    if (nsLight && (nsLight.state === 'red' || nsLight.state === 'yellow')) {
      // Northbound vehicles (moving in -z direction)
      if (direction === 'north' && z > 4 && z < 12 && x > -3 && x < 3) return true
      // Southbound vehicles (moving in +z direction)
      if (direction === 'south' && z < -4 && z > -12 && x > -3 && x < 3) return true
    }
    
    // Check East-West traffic light (light-ew)
    const ewLight = lights.find(l => l.id === 'light-ew')
    if (ewLight && (ewLight.state === 'red' || ewLight.state === 'yellow')) {
      // Eastbound vehicles (moving in +x direction)
      if (direction === 'east' && x > -12 && x < -4 && z > -3 && z < 3) return true
      // Westbound vehicles (moving in -x direction)
      if (direction === 'west' && x < 12 && x > 4 && z > -3 && z < 3) return true
    }
    
    return false
  }
  
  // Helper: Check for vehicle ahead (collision avoidance with better spacing)
  const getVehicleAhead = (vehicle: any, allVehicles: any[]) => {
    const { position, direction } = vehicle
    const [x, z] = [position[0], position[2]]
    const detectionRange = 6.0 // Increased look ahead distance for better spacing
    const laneWidth = 2.0 // Narrower lane detection for precision
    
    return allVehicles.find(other => {
      if (other.id === vehicle.id) return false
      const [ox, oz] = [other.position[0], other.position[2]]
      
      let distance = 0
      let inLane = false
      
      switch (direction) {
        case 'north':
          distance = z - oz
          inLane = Math.abs(ox - x) < laneWidth && oz < z && distance > 0 && distance < detectionRange
          return inLane
        case 'south':
          distance = oz - z
          inLane = Math.abs(ox - x) < laneWidth && oz > z && distance > 0 && distance < detectionRange
          return inLane
        case 'east':
          distance = ox - x
          inLane = Math.abs(oz - z) < laneWidth && ox > x && distance > 0 && distance < detectionRange
          return inLane
        case 'west':
          distance = x - ox
          inLane = Math.abs(oz - z) < laneWidth && ox < x && distance > 0 && distance < detectionRange
          return inLane
        default:
          return false
      }
    })
  }
  
  useFrame((state, delta) => {
    if (!isRunning) return
    
    frameCount.current++
    const fps = Math.round(1 / delta)
    
    // Update FPS every 30 frames
    if (frameCount.current % 30 === 0) {
      updateMetrics(fps)
    }
    
    // Spawn new vehicles with varying spawn rates based on traffic conditions
    const time = state.clock.getElapsedTime()
    const spawnInterval = 1.5 + Math.random() * 1.5 // Random 1.5-3 seconds
    
    if (time - lastSpawn.current > spawnInterval) {
      const spawnPoints = [
        { pos: [0, 0.75, -18], dir: 'north' },
        { pos: [0, 0.75, 18], dir: 'south' },
        { pos: [-18, 0.75, 0], dir: 'east' },
        { pos: [18, 0.75, 0], dir: 'west' },
      ]
      
      const spawn = spawnPoints[Math.floor(Math.random() * spawnPoints.length)]
      const types = ['car', 'car', 'car', 'car', 'truck', 'bus'] // More cars
      const colors = ['#ff0000', '#0000ff', '#ffff00', '#00ff00', '#ff00ff', '#00ffff', '#ffffff', '#ff8800']
      
      const vehicleType = types[Math.floor(Math.random() * types.length)] as any
      const maxSpeed = vehicleType === 'bus' ? 3 : vehicleType === 'truck' ? 3.5 : 4.5
      
      addVehicle({
        id: `vehicle-${Date.now()}-${Math.random()}`,
        position: spawn.pos as [number, number, number],
        speed: maxSpeed,
        direction: spawn.dir as any,
        type: vehicleType,
        color: colors[Math.floor(Math.random() * colors.length)]
      })
      
      lastSpawn.current = time
    }
    
    // Update vehicle positions with realistic traffic behavior
    vehicles.forEach(vehicle => {
      const newPos = [...vehicle.position] as [number, number, number]
      let currentSpeed = vehicle.speed
      
      // Check if should stop at red light
      const mustStop = shouldStopAtLight(vehicle, trafficLights)
      
      // Check for vehicle ahead
      const vehicleAhead = getVehicleAhead(vehicle, vehicles)
      
      // Better speed adjustment for smooth traffic flow
      if (mustStop) {
        // Gradual braking as approaching red light
        const [x, z] = [vehicle.position[0], vehicle.position[2]]
        const distToCenter = Math.sqrt(x * x + z * z)
        if (distToCenter < 5) {
          currentSpeed = 0 // Full stop at intersection
        } else if (distToCenter < 8) {
          currentSpeed = vehicle.speed * 0.2 // Slow braking
        }
      } else if (vehicleAhead) {
        // Calculate distance to vehicle ahead
        const [vx, vz] = [vehicle.position[0], vehicle.position[2]]
        const [ox, oz] = [vehicleAhead.position[0], vehicleAhead.position[2]]
        const distance = Math.sqrt((vx - ox) ** 2 + (vz - oz) ** 2)
        
        // Adaptive speed based on distance (maintain 3-unit minimum spacing)
        if (distance < 3) {
          currentSpeed = 0 // Stop if too close
        } else if (distance < 4) {
          currentSpeed = vehicle.speed * 0.2 // Very slow
        } else if (distance < 5) {
          currentSpeed = vehicle.speed * 0.5 // Half speed
        } else {
          currentSpeed = vehicle.speed * 0.7 // Slightly reduced
        }
      }
      
      const actualSpeed = delta * currentSpeed
      const isStopped = currentSpeed === 0 || currentSpeed < 0.5
      
      // Update position based on direction
      switch (vehicle.direction) {
        case 'north':
          newPos[2] -= actualSpeed
          break
        case 'south':
          newPos[2] += actualSpeed
          break
        case 'east':
          newPos[0] += actualSpeed
          break
        case 'west':
          newPos[0] -= actualSpeed
          break
      }
      
      // Remove vehicles that are off screen
      if (Math.abs(newPos[0]) > 20 || Math.abs(newPos[2]) > 20) {
        removeVehicle(vehicle.id)
      } else {
        updateVehicle(vehicle.id, { position: newPos, isStopped })
      }
    })
    
    // Update traffic lights with coordinated timing
    trafficLights.forEach(light => {
      const newTimer = light.timer + delta
      const cycleTime = light.cycleTime[light.state]
      
      if (newTimer >= cycleTime) {
        let newState = light.state
        if (light.state === 'green') newState = 'yellow'
        else if (light.state === 'yellow') newState = 'red'
        else if (light.state === 'red') newState = 'green'
        
        updateTrafficLight(light.id, { state: newState, timer: 0 })
      } else {
        updateTrafficLight(light.id, { timer: newTimer })
      }
    })
    
    // Update camera metrics with detailed analysis
    const cameras = useSimulationStore.getState().cameras
    cameras.forEach(camera => {
      const vehiclesInRange = vehicles.filter(v => {
        const dist = Math.sqrt(
          Math.pow(v.position[0] - camera.position[0], 2) +
          Math.pow(v.position[2] - camera.position[2], 2)
        )
        return dist < 10
      })
      
      // Count stopped vehicles (queue length)
      const stoppedVehicles = vehiclesInRange.filter(v => {
        const stopped = shouldStopAtLight(v, trafficLights) || getVehicleAhead(v, vehicles)
        return stopped
      })
      
      const movingVehicles = vehiclesInRange.filter(v => {
        const stopped = shouldStopAtLight(v, trafficLights) || getVehicleAhead(v, vehicles)
        return !stopped
      })
      
      updateCamera(camera.id, {
        vehicleCount: vehiclesInRange.length,
        queueLength: stoppedVehicles.length,
        avgSpeed: movingVehicles.length > 0 
          ? movingVehicles.reduce((acc, v) => acc + v.speed, 0) / movingVehicles.length 
          : 0
      })
    })
  })
  
  return null
}

// Main 3D Scene Component
function Scene() {
  const { vehicles, cameras, trafficLights } = useSimulationStore()
  
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight
        position={[10, 20, 10]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-20}
        shadow-camera-right={20}
        shadow-camera-top={20}
        shadow-camera-bottom={-20}
      />
      
      {/* Sky */}
      <Sky sunPosition={[100, 20, 100]} />
      
      {/* Ground */}
      <mesh position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[50, 50]} />
        <meshStandardMaterial color="#1a1a1a" />
      </mesh>
      
      {/* Road Intersection */}
      <RoadIntersection />
      
      {/* Vehicles */}
      {vehicles.map(vehicle => (
        <Vehicle
          key={vehicle.id}
          position={vehicle.position}
          color={vehicle.color}
          type={vehicle.type}
          isStopped={vehicle.isStopped}
        />
      ))}
      
      {/* Traffic Lights */}
      {trafficLights.map(light => (
        <TrafficLight3D
          key={light.id}
          position={light.position}
          state={light.state}
        />
      ))}
      
      {/* Cameras */}
      {cameras.map(camera => (
        <CameraMarker
          key={camera.id}
          position={camera.position}
          name={camera.name}
          active={camera.active}
        />
      ))}
      
      {/* Animation Loop */}
      <SimulationLoop />
      
      {/* Camera Controls */}
      <OrbitControls
        makeDefault
        minDistance={10}
        maxDistance={50}
        maxPolarAngle={Math.PI / 2.2}
      />
      
      {/* Camera */}
      <PerspectiveCamera makeDefault position={[20, 15, 20]} fov={60} />
    </>
  )
}

// Main Component
export default function TrafficSimulation() {
  const [mounted, setMounted] = useState(false)
  
  useEffect(() => {
    setMounted(true)
  }, [])
  
  if (!mounted) {
    return (
      <div className="w-full h-[600px] bg-gray-900 flex items-center justify-center">
        <div className="text-gray-400">Loading 3D Scene...</div>
      </div>
    )
  }
  
  return (
    <div className="w-full h-[600px] bg-gradient-to-b from-blue-900/20 to-gray-900">
      <Canvas shadows>
        <Scene />
      </Canvas>
    </div>
  )
}
