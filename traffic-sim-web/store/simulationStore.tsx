'use client'

import { create } from 'zustand'
import React from 'react'

export interface Vehicle {
  id: string
  position: [number, number, number]
  speed: number
  direction: 'north' | 'south' | 'east' | 'west'
  type: 'car' | 'truck' | 'bus'
  color: string
  isStopped?: boolean
}

export interface Camera {
  id: string
  name: string
  position: [number, number, number]
  vehicleCount: number
  queueLength: number
  avgSpeed: number
  active: boolean
}

export interface TrafficLight {
  id: string
  name: string
  state: 'red' | 'yellow' | 'green'
  position: [number, number, number]
  timer: number
  cycleTime: { red: number; yellow: number; green: number }
}

interface SimulationState {
  isRunning: boolean
  isPaused: boolean
  vehicles: Vehicle[]
  cameras: Camera[]
  trafficLights: TrafficLight[]
  fps: number
  totalVehicles: number
  avgQueueLength: number
  avgSpeed: number
  
  // Actions
  toggleSimulation: () => void
  pauseSimulation: () => void
  resetSimulation: () => void
  toggleCamera: (id: string) => void
  addVehicle: (vehicle: Vehicle) => void
  removeVehicle: (id: string) => void
  updateVehicle: (id: string, updates: Partial<Vehicle>) => void
  updateCamera: (id: string, updates: Partial<Camera>) => void
  updateTrafficLight: (id: string, updates: Partial<TrafficLight>) => void
  updateMetrics: (fps: number) => void
  reset: () => void
}

const initialCameras: Camera[] = [
  { id: 'cam-north', name: 'North Approach', position: [0, 5, 15], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-south', name: 'South Approach', position: [0, 5, -15], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-east', name: 'East Approach', position: [15, 5, 0], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-west', name: 'West Approach', position: [-15, 5, 0], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-center', name: 'Center Intersection', position: [0, 8, 0], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-ne', name: 'Northeast Monitor', position: [10, 6, 10], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
  { id: 'cam-sw', name: 'Southwest Monitor', position: [-10, 6, -10], vehicleCount: 0, queueLength: 0, avgSpeed: 0, active: true },
]

const initialTrafficLights: TrafficLight[] = [
  { id: 'light-ns', name: 'North-South Main', state: 'green', position: [2, 3, 0], timer: 0, cycleTime: { green: 30, yellow: 5, red: 35 } },
  { id: 'light-ew', name: 'East-West Cross', state: 'red', position: [0, 3, 2], timer: 0, cycleTime: { green: 25, yellow: 5, red: 40 } },
  { id: 'light-ped', name: 'Pedestrian', state: 'red', position: [-2, 3, -2], timer: 0, cycleTime: { green: 15, yellow: 3, red: 52 } },
]

export const useSimulationStore = create<SimulationState>((set) => ({
  isRunning: false,
  isPaused: false,
  vehicles: [],
  cameras: initialCameras,
  trafficLights: initialTrafficLights,
  fps: 60,
  totalVehicles: 0,
  avgQueueLength: 0,
  avgSpeed: 0,

  toggleSimulation: () => set((state) => ({ 
    isRunning: !state.isRunning,
    isPaused: false
  })),
  
  pauseSimulation: () => set((state) => ({ isPaused: !state.isPaused })),
  
  resetSimulation: () => set({
    isRunning: false,
    isPaused: false,
    vehicles: [],
    cameras: initialCameras,
    trafficLights: initialTrafficLights,
    totalVehicles: 0,
    avgQueueLength: 0,
    avgSpeed: 0,
  }),
  
  toggleCamera: (id) => set((state) => ({
    cameras: state.cameras.map(c => 
      c.id === id ? { ...c, active: !c.active } : c
    ),
  })),
  
  addVehicle: (vehicle) => set((state) => ({
    vehicles: [...state.vehicles, vehicle],
    totalVehicles: state.totalVehicles + 1,
  })),
  
  removeVehicle: (id) => set((state) => ({
    vehicles: state.vehicles.filter(v => v.id !== id),
  })),
  
  updateVehicle: (id, updates) => set((state) => ({
    vehicles: state.vehicles.map(v => v.id === id ? { ...v, ...updates } : v),
  })),
  
  updateCamera: (id, updates) => set((state) => ({
    cameras: state.cameras.map(c => c.id === id ? { ...c, ...updates } : c),
  })),
  
  updateTrafficLight: (id, updates) => set((state) => ({
    trafficLights: state.trafficLights.map(t => t.id === id ? { ...t, ...updates } : t),
  })),
  
  updateMetrics: (fps) => set((state) => {
    const avgQueueLength = state.cameras.reduce((acc, c) => acc + c.queueLength, 0) / state.cameras.length
    const avgSpeed = state.vehicles.reduce((acc, v) => acc + v.speed, 0) / (state.vehicles.length || 1)
    return { fps, avgQueueLength, avgSpeed }
  }),
  
  reset: () => set({
    isRunning: false,
    isPaused: false,
    vehicles: [],
    cameras: initialCameras,
    trafficLights: initialTrafficLights,
    totalVehicles: 0,
    avgQueueLength: 0,
    avgSpeed: 0,
  }),
}))
