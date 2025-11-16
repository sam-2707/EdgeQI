"""
Enhanced Multi-Edge Collaboration System with Advanced Distributed Systems Concepts
Implements consensus protocols, leader election, deadlock detection, and mutual exclusion
"""

import asyncio
import time
import logging
import threading
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from enum import Enum
from collections import defaultdict, deque
import hashlib
import uuid

logger = logging.getLogger(__name__)

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"
    FAILED = "failed"

class ConsensusType(Enum):
    SIMPLE_MAJORITY = "simple_majority"
    BYZANTINE_FAULT_TOLERANT = "byzantine_fault_tolerant"
    RAFT = "raft"

class MessageType(Enum):
    VOTE_REQUEST = "vote_request"
    VOTE_RESPONSE = "vote_response"
    APPEND_ENTRIES = "append_entries"
    APPEND_RESPONSE = "append_response"
    CONSENSUS_PROPOSAL = "consensus_proposal"
    CONSENSUS_VOTE = "consensus_vote"
    CONSENSUS_COMMIT = "consensus_commit"
    DEADLOCK_DETECTION = "deadlock_detection"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_RELEASE = "resource_release"

@dataclass
class EdgeNode:
    """Represents an edge node in the distributed system"""
    node_id: str
    ip_address: str
    port: int
    capabilities: Dict[str, Any]
    last_heartbeat: float = 0.0
    state: NodeState = NodeState.FOLLOWER
    current_term: int = 0
    voted_for: Optional[str] = None
    is_alive: bool = True
    load_score: float = 0.0
    energy_level: float = 100.0

@dataclass
class ConsensusProposal:
    """Consensus proposal for distributed decision making"""
    proposal_id: str
    proposer_id: str
    proposal_type: str  # e.g., "traffic_signal_change", "load_balancing"
    proposal_data: Dict[str, Any]
    timestamp: float
    deadline: float
    required_votes: int
    received_votes: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected, timeout

@dataclass
class ResourceLock:
    """Distributed resource lock for mutual exclusion"""
    resource_id: str
    holder_node: str
    lock_type: str  # shared, exclusive
    acquired_time: float
    timeout: float
    waiters: List[str] = field(default_factory=list)

@dataclass
class DeadlockEdge:
    """Edge in deadlock detection graph"""
    from_node: str
    to_node: str
    resource_id: str
    timestamp: float

class DistributedEdgeCollaboration:
    """
    Advanced multi-edge collaboration system implementing:
    - RAFT consensus protocol with leader election
    - Byzantine Fault Tolerance for critical decisions
    - Deadlock detection and prevention using wait-for graphs
    - Distributed mutual exclusion with priority ordering
    - Load balancing and resource optimization
    """
    
    def __init__(self, 
                 node_id: str, 
                 node_ip: str = "localhost", 
                 node_port: int = 8000):
        """
        Initialize distributed collaboration system
        
        Args:
            node_id: Unique identifier for this edge node
            node_ip: IP address of this node
            node_port: Port for inter-node communication
        """
        self.node_id = node_id
        self.node_ip = node_ip
        self.node_port = node_port
        
        # Node state management
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.leader_id: Optional[str] = None
        self.last_heartbeat_received = time.time()
        
        # Network topology
        self.peer_nodes: Dict[str, EdgeNode] = {}
        self.failed_nodes: Set[str] = set()
        
        # Consensus management
        self.active_proposals: Dict[str, ConsensusProposal] = {}
        self.consensus_history: List[Dict] = []
        self.consensus_type = ConsensusType.RAFT
        
        # Distributed locking for mutual exclusion
        self.local_locks: Dict[str, ResourceLock] = {}
        self.lock_requests: deque = deque()
        self.resource_allocation: Dict[str, str] = {}  # resource_id -> holder_node
        
        # Deadlock detection
        self.wait_for_graph: Dict[str, List[str]] = defaultdict(list)
        self.deadlock_detection_enabled = True
        self.last_deadlock_check = time.time()
        
        # Performance metrics
        self.metrics = {
            'consensus_success_rate': 0.0,
            'average_consensus_time': 0.0,
            'leader_elections_count': 0,
            'deadlocks_detected': 0,
            'deadlocks_resolved': 0,
            'mutual_exclusion_conflicts': 0,
            'load_balancing_decisions': 0
        }
        
        # Threading and async management
        self.collaboration_lock = threading.Lock()
        self.is_running = False
        self.background_tasks: List[asyncio.Task] = []
        
        # Callbacks
        self.on_leader_elected: Optional[Callable] = None
        self.on_consensus_reached: Optional[Callable] = None
        self.on_deadlock_detected: Optional[Callable] = None
        
    async def start_collaboration(self):
        """Start the distributed collaboration system"""
        if self.is_running:
            return
            
        self.is_running = True
        logger.info(f"Starting distributed collaboration for node {self.node_id}")
        
        # Start background tasks
        self.background_tasks = [
            asyncio.create_task(self._heartbeat_service()),
            asyncio.create_task(self._consensus_service()),
            asyncio.create_task(self._deadlock_detection_service()),
            asyncio.create_task(self._load_balancing_service()),
            asyncio.create_task(self._leader_election_service())
        ]
        
        await asyncio.gather(*self.background_tasks, return_exceptions=True)
    
    async def stop_collaboration(self):
        """Stop the collaboration system gracefully"""
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
        
        # Release all local locks
        await self._release_all_locks()
        
        logger.info(f"Stopped distributed collaboration for node {self.node_id}")
    
    # ==========================================
    # LEADER ELECTION (RAFT ALGORITHM)
    # ==========================================
    
    async def _leader_election_service(self):
        """Background service for leader election"""
        while self.is_running:
            try:
                # Check if leader is alive
                if self.state == NodeState.FOLLOWER:
                    if time.time() - self.last_heartbeat_received > 5.0:  # 5 second timeout
                        await self._start_election()
                
                # Send heartbeats if leader
                elif self.state == NodeState.LEADER:
                    await self._send_heartbeats()
                
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Error in leader election service: {e}")
    
    async def _start_election(self):
        """
        Start leader election process (RAFT algorithm)
        Implements distributed consensus for leader selection
        """
        with self.collaboration_lock:
            self.state = NodeState.CANDIDATE
            self.current_term += 1
            self.voted_for = self.node_id
            self.metrics['leader_elections_count'] += 1
        
        logger.info(f"Node {self.node_id} starting election for term {self.current_term}")
        
        # Request votes from all peers
        votes_received = 1  # Vote for self
        total_nodes = len(self.peer_nodes) + 1
        
        vote_tasks = []
        for peer_id, peer_node in self.peer_nodes.items():
            if peer_id not in self.failed_nodes:
                task = asyncio.create_task(self._request_vote(peer_id, peer_node))
                vote_tasks.append(task)
        
        # Wait for vote responses
        if vote_tasks:
            vote_responses = await asyncio.gather(*vote_tasks, return_exceptions=True)
            
            for response in vote_responses:
                if isinstance(response, bool) and response:
                    votes_received += 1
        
        # Check if won election
        if votes_received > total_nodes / 2:
            await self._become_leader()
        else:
            with self.collaboration_lock:
                self.state = NodeState.FOLLOWER
                self.voted_for = None
            logger.info(f"Node {self.node_id} lost election for term {self.current_term}")
    
    async def _request_vote(self, peer_id: str, peer_node: EdgeNode) -> bool:
        """
        Request vote from a peer node
        
        Args:
            peer_id: ID of the peer node
            peer_node: Peer node information
            
        Returns:
            True if vote granted, False otherwise
        """
        try:
            # In real implementation, send network message
            # For simulation, use node capability and load as decision factors
            
            # Simulate network communication delay
            await asyncio.sleep(0.1 + (hash(peer_id) % 100) / 1000)
            
            # Decision logic: vote for node with better capabilities and lower load
            my_score = self._calculate_leadership_score()
            peer_score = peer_node.load_score + (100 - peer_node.energy_level) * 0.01
            
            # Vote granted if this node has better score
            vote_granted = my_score < peer_score
            
            logger.debug(f"Vote request to {peer_id}: {'granted' if vote_granted else 'denied'}")
            return vote_granted
            
        except Exception as e:
            logger.error(f"Error requesting vote from {peer_id}: {e}")
            return False
    
    def _calculate_leadership_score(self) -> float:
        """
        Calculate leadership capability score (lower is better)
        Considers load, energy, and capabilities
        """
        load_penalty = getattr(self, 'current_load', 50) * 0.01  # 0-1
        energy_penalty = (100 - getattr(self, 'energy_level', 80)) * 0.01  # 0-1
        capability_bonus = len(getattr(self, 'capabilities', {})) * -0.05  # Negative = better
        
        return load_penalty + energy_penalty + capability_bonus
    
    async def _become_leader(self):
        """Become the leader and start sending heartbeats"""
        with self.collaboration_lock:
            self.state = NodeState.LEADER
            self.leader_id = self.node_id
        
        logger.info(f"Node {self.node_id} became leader for term {self.current_term}")
        
        if self.on_leader_elected:
            self.on_leader_elected(self.node_id, self.current_term)
    
    async def _send_heartbeats(self):
        """Send heartbeats to all followers"""
        heartbeat_tasks = []
        
        for peer_id, peer_node in self.peer_nodes.items():
            if peer_id not in self.failed_nodes:
                task = asyncio.create_task(self._send_heartbeat(peer_id, peer_node))
                heartbeat_tasks.append(task)
        
        if heartbeat_tasks:
            await asyncio.gather(*heartbeat_tasks, return_exceptions=True)
    
    async def _send_heartbeat(self, peer_id: str, peer_node: EdgeNode):
        """Send heartbeat to specific peer"""
        try:
            # In real implementation, send network message
            # Update peer's last heartbeat time
            peer_node.last_heartbeat = time.time()
            
        except Exception as e:
            logger.error(f"Error sending heartbeat to {peer_id}: {e}")
            # Mark node as potentially failed
            if time.time() - peer_node.last_heartbeat > 10.0:
                self.failed_nodes.add(peer_id)
    
    # ==========================================
    # CONSENSUS PROTOCOLS
    # ==========================================
    
    async def _consensus_service(self):
        """Background service for consensus management"""
        while self.is_running:
            try:
                # Process active proposals
                await self._process_consensus_proposals()
                
                # Clean up expired proposals
                self._cleanup_expired_proposals()
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error in consensus service: {e}")
    
    async def propose_consensus_decision(self, 
                                       proposal_type: str, 
                                       proposal_data: Dict[str, Any],
                                       timeout_seconds: float = 30.0) -> Dict[str, Any]:
        """
        Propose a decision for consensus voting
        
        Args:
            proposal_type: Type of decision (e.g., "traffic_signal", "load_balancing")
            proposal_data: Data for the proposal
            timeout_seconds: Maximum time to wait for consensus
            
        Returns:
            Dictionary with consensus result
        """
        proposal_id = str(uuid.uuid4())
        timestamp = time.time()
        
        # Calculate required votes based on consensus type
        total_nodes = len(self.peer_nodes) + 1
        if self.consensus_type == ConsensusType.BYZANTINE_FAULT_TOLERANT:
            # Byzantine fault tolerance: need 2f+1 votes where f = ⌊(n-1)/3⌋
            f = (total_nodes - 1) // 3
            required_votes = 2 * f + 1
        else:
            # Simple majority
            required_votes = (total_nodes // 2) + 1
        
        proposal = ConsensusProposal(
            proposal_id=proposal_id,
            proposer_id=self.node_id,
            proposal_type=proposal_type,
            proposal_data=proposal_data,
            timestamp=timestamp,
            deadline=timestamp + timeout_seconds,
            required_votes=required_votes
        )
        
        with self.collaboration_lock:
            self.active_proposals[proposal_id] = proposal
        
        logger.info(f"Proposed consensus decision: {proposal_type} (ID: {proposal_id})")
        
        # Broadcast proposal to all peers
        await self._broadcast_consensus_proposal(proposal)
        
        # Wait for consensus or timeout
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            with self.collaboration_lock:
                if proposal.status != "pending":
                    break
            await asyncio.sleep(0.1)
        
        # Finalize result
        with self.collaboration_lock:
            if proposal.status == "pending":
                proposal.status = "timeout"
            
            result = {
                'proposal_id': proposal_id,
                'status': proposal.status,
                'votes_received': len(proposal.received_votes),
                'required_votes': proposal.required_votes,
                'duration': time.time() - timestamp,
                'proposal_type': proposal_type
            }
            
            # Update metrics
            if proposal.status == "approved":
                self.metrics['consensus_success_rate'] = (
                    self.metrics['consensus_success_rate'] * 0.9 + 0.1
                )
            else:
                self.metrics['consensus_success_rate'] *= 0.9
            
            # Update average consensus time
            self.metrics['average_consensus_time'] = (
                self.metrics['average_consensus_time'] * 0.9 + 
                result['duration'] * 0.1
            )
            
            # Add to history
            self.consensus_history.append(result)
            if len(self.consensus_history) > 100:
                self.consensus_history.pop(0)
        
        if self.on_consensus_reached:
            self.on_consensus_reached(result)
        
        return result
    
    async def _broadcast_consensus_proposal(self, proposal: ConsensusProposal):
        """Broadcast consensus proposal to all peer nodes"""
        broadcast_tasks = []
        
        for peer_id, peer_node in self.peer_nodes.items():
            if peer_id not in self.failed_nodes:
                task = asyncio.create_task(
                    self._send_consensus_proposal(peer_id, peer_node, proposal)
                )
                broadcast_tasks.append(task)
        
        if broadcast_tasks:
            await asyncio.gather(*broadcast_tasks, return_exceptions=True)
    
    async def _send_consensus_proposal(self, 
                                     peer_id: str, 
                                     peer_node: EdgeNode, 
                                     proposal: ConsensusProposal):
        """Send consensus proposal to specific peer"""
        try:
            # Simulate network communication
            await asyncio.sleep(0.05 + (hash(peer_id) % 50) / 1000)
            
            # Simulate peer vote based on proposal type and node state
            vote = self._simulate_peer_vote(peer_id, peer_node, proposal)
            
            if vote:
                with self.collaboration_lock:
                    if peer_id not in proposal.received_votes:
                        proposal.received_votes.append(peer_id)
                        
                        # Check if consensus reached
                        if len(proposal.received_votes) >= proposal.required_votes:
                            proposal.status = "approved"
                            logger.info(f"Consensus reached for proposal {proposal.proposal_id}")
            
        except Exception as e:
            logger.error(f"Error sending consensus proposal to {peer_id}: {e}")
    
    def _simulate_peer_vote(self, 
                           peer_id: str, 
                           peer_node: EdgeNode, 
                           proposal: ConsensusProposal) -> bool:
        """
        Simulate peer vote decision
        In real implementation, this would be the peer's decision logic
        """
        # Base approval probability
        approval_prob = 0.8
        
        # Adjust based on peer node state
        if peer_node.energy_level < 20:
            approval_prob *= 0.5  # Low energy nodes less likely to approve
        
        if peer_node.load_score > 80:
            approval_prob *= 0.6  # High load nodes less likely to approve
        
        # Adjust based on proposal type
        if proposal.proposal_type == "emergency":
            approval_prob = 0.95  # High approval for emergency decisions
        elif proposal.proposal_type == "load_balancing":
            approval_prob = 0.7  # Moderate approval for load balancing
        
        return hash(f"{peer_id}{proposal.proposal_id}") % 100 < approval_prob * 100
    
    async def _process_consensus_proposals(self):
        """Process active consensus proposals"""
        current_time = time.time()
        
        with self.collaboration_lock:
            for proposal_id, proposal in list(self.active_proposals.items()):
                if proposal.status == "pending":
                    # Check for timeout
                    if current_time > proposal.deadline:
                        proposal.status = "timeout"
                        logger.warning(f"Consensus proposal {proposal_id} timed out")
    
    def _cleanup_expired_proposals(self):
        """Clean up old proposals from memory"""
        current_time = time.time()
        
        with self.collaboration_lock:
            expired_proposals = [
                pid for pid, proposal in self.active_proposals.items()
                if current_time - proposal.timestamp > 300  # 5 minutes
            ]
            
            for pid in expired_proposals:
                del self.active_proposals[pid]
    
    # ==========================================
    # DISTRIBUTED MUTUAL EXCLUSION
    # ==========================================
    
    async def request_resource_lock(self, 
                                   resource_id: str, 
                                   lock_type: str = "exclusive",
                                   timeout_seconds: float = 60.0) -> bool:
        """
        Request distributed lock for resource (implements mutual exclusion)
        
        Args:
            resource_id: ID of the resource to lock
            lock_type: "shared" or "exclusive"
            timeout_seconds: Maximum time to wait for lock
            
        Returns:
            True if lock acquired, False if timeout or conflict
        """
        logger.info(f"Requesting {lock_type} lock for resource {resource_id}")
        
        # Check for potential deadlock before making request
        if self.deadlock_detection_enabled:
            potential_deadlock = self._check_potential_deadlock(resource_id)
            if potential_deadlock:
                logger.warning(f"Potential deadlock detected for resource {resource_id}")
                return False
        
        # Add to wait-for graph
        current_holder = self.resource_allocation.get(resource_id)
        if current_holder and current_holder != self.node_id:
            self.wait_for_graph[self.node_id].append(current_holder)
        
        start_time = time.time()
        
        # Try to acquire lock locally first
        if resource_id not in self.local_locks:
            # Resource available locally
            lock = ResourceLock(
                resource_id=resource_id,
                holder_node=self.node_id,
                lock_type=lock_type,
                acquired_time=time.time(),
                timeout=time.time() + timeout_seconds
            )
            
            self.local_locks[resource_id] = lock
            self.resource_allocation[resource_id] = self.node_id
            
            # Notify other nodes about lock acquisition
            await self._broadcast_lock_acquisition(resource_id, lock_type)
            
            logger.info(f"Acquired {lock_type} lock for resource {resource_id}")
            return True
        
        else:
            # Resource locked, add to waiters
            existing_lock = self.local_locks[resource_id]
            
            # Check if shared locks are compatible
            if (lock_type == "shared" and existing_lock.lock_type == "shared"):
                existing_lock.waiters.append(self.node_id)
                logger.info(f"Shared lock granted for resource {resource_id}")
                return True
            
            # Wait for exclusive lock to be released
            existing_lock.waiters.append(self.node_id)
            
            while time.time() - start_time < timeout_seconds:
                if resource_id not in self.local_locks:
                    # Try to acquire again
                    return await self.request_resource_lock(resource_id, lock_type, 
                                                          timeout_seconds - (time.time() - start_time))
                
                await asyncio.sleep(0.1)
            
            # Timeout - remove from waiters
            if resource_id in self.local_locks:
                existing_lock = self.local_locks[resource_id]
                if self.node_id in existing_lock.waiters:
                    existing_lock.waiters.remove(self.node_id)
            
            # Remove from wait-for graph
            if current_holder in self.wait_for_graph[self.node_id]:
                self.wait_for_graph[self.node_id].remove(current_holder)
            
            logger.warning(f"Timeout waiting for {lock_type} lock on resource {resource_id}")
            return False
    
    async def release_resource_lock(self, resource_id: str):
        """
        Release distributed lock for resource
        
        Args:
            resource_id: ID of the resource to unlock
        """
        if resource_id not in self.local_locks:
            logger.warning(f"Attempted to release non-existent lock for resource {resource_id}")
            return
        
        lock = self.local_locks[resource_id]
        
        if lock.holder_node != self.node_id:
            logger.warning(f"Attempted to release lock not owned by this node: {resource_id}")
            return
        
        # Remove lock
        del self.local_locks[resource_id]
        if resource_id in self.resource_allocation:
            del self.resource_allocation[resource_id]
        
        # Remove from wait-for graph
        for waiter_list in self.wait_for_graph.values():
            if self.node_id in waiter_list:
                waiter_list.remove(self.node_id)
        
        # Notify waiters
        if lock.waiters:
            # Give priority to first waiter
            next_holder = lock.waiters[0]
            logger.info(f"Lock for resource {resource_id} passed to {next_holder}")
        
        # Broadcast lock release
        await self._broadcast_lock_release(resource_id)
        
        logger.info(f"Released lock for resource {resource_id}")
    
    async def _broadcast_lock_acquisition(self, resource_id: str, lock_type: str):
        """Notify other nodes about lock acquisition"""
        # In real implementation, send network messages
        logger.debug(f"Broadcasting lock acquisition: {resource_id} ({lock_type})")
    
    async def _broadcast_lock_release(self, resource_id: str):
        """Notify other nodes about lock release"""
        # In real implementation, send network messages
        logger.debug(f"Broadcasting lock release: {resource_id}")
    
    async def _release_all_locks(self):
        """Release all locks held by this node"""
        for resource_id in list(self.local_locks.keys()):
            await self.release_resource_lock(resource_id)
    
    # ==========================================
    # DEADLOCK DETECTION AND PREVENTION
    # ==========================================
    
    async def _deadlock_detection_service(self):
        """Background service for deadlock detection"""
        while self.is_running:
            try:
                if self.deadlock_detection_enabled:
                    deadlocks = self._detect_deadlocks()
                    
                    if deadlocks:
                        logger.warning(f"Deadlocks detected: {len(deadlocks)}")
                        self.metrics['deadlocks_detected'] += len(deadlocks)
                        
                        for deadlock_cycle in deadlocks:
                            await self._resolve_deadlock(deadlock_cycle)
                        
                        if self.on_deadlock_detected:
                            self.on_deadlock_detected(deadlocks)
                
                await asyncio.sleep(2.0)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in deadlock detection service: {e}")
    
    def _detect_deadlocks(self) -> List[List[str]]:
        """
        Detect deadlocks using cycle detection in wait-for graph
        
        Returns:
            List of deadlock cycles (each cycle is a list of node IDs)
        """
        deadlocks = []
        visited = set()
        
        def dfs_cycle_detection(node: str, path: List[str], in_path: Set[str]):
            if node in in_path:
                # Found cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                deadlocks.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            in_path.add(node)
            path.append(node)
            
            # Explore neighbors in wait-for graph
            for neighbor in self.wait_for_graph.get(node, []):
                dfs_cycle_detection(neighbor, path.copy(), in_path.copy())
        
        # Check all nodes
        for node_id in self.wait_for_graph:
            if node_id not in visited:
                dfs_cycle_detection(node_id, [], set())
        
        return deadlocks
    
    def _check_potential_deadlock(self, resource_id: str) -> bool:
        """
        Check if requesting a resource could cause deadlock
        
        Args:
            resource_id: Resource being requested
            
        Returns:
            True if potential deadlock, False otherwise
        """
        current_holder = self.resource_allocation.get(resource_id)
        
        if not current_holder or current_holder == self.node_id:
            return False
        
        # Temporarily add edge and check for cycles
        temp_graph = dict(self.wait_for_graph)
        if self.node_id not in temp_graph:
            temp_graph[self.node_id] = []
        
        temp_graph[self.node_id].append(current_holder)
        
        # Simple cycle detection
        visited = set()
        
        def has_cycle(node: str, path: Set[str]) -> bool:
            if node in path:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            path.add(node)
            
            for neighbor in temp_graph.get(node, []):
                if has_cycle(neighbor, path.copy()):
                    return True
            
            return False
        
        return has_cycle(self.node_id, set())
    
    async def _resolve_deadlock(self, deadlock_cycle: List[str]):
        """
        Resolve deadlock by breaking the cycle
        Uses priority-based preemption
        
        Args:
            deadlock_cycle: List of nodes involved in deadlock
        """
        logger.info(f"Resolving deadlock cycle: {deadlock_cycle}")
        
        # Find lowest priority node in cycle (by node ID for deterministic behavior)
        victim_node = min(deadlock_cycle)
        
        if victim_node == self.node_id:
            # This node is the victim - release some locks
            resources_to_release = []
            
            for resource_id, lock in self.local_locks.items():
                if lock.holder_node == self.node_id and lock.waiters:
                    resources_to_release.append(resource_id)
                    break  # Release one lock to break cycle
            
            for resource_id in resources_to_release:
                await self.release_resource_lock(resource_id)
                logger.info(f"Released resource {resource_id} to resolve deadlock")
        
        self.metrics['deadlocks_resolved'] += 1
    
    # ==========================================
    # LOAD BALANCING AND OPTIMIZATION
    # ==========================================
    
    async def _load_balancing_service(self):
        """Background service for load balancing coordination"""
        while self.is_running:
            try:
                if self.state == NodeState.LEADER:
                    await self._coordinate_load_balancing()
                
                await asyncio.sleep(10.0)  # Balance every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in load balancing service: {e}")
    
    async def _coordinate_load_balancing(self):
        """
        Coordinate load balancing across edge nodes (leader only)
        """
        if self.state != NodeState.LEADER:
            return
        
        # Collect load information from all nodes
        node_loads = {}
        
        for peer_id, peer_node in self.peer_nodes.items():
            if peer_id not in self.failed_nodes:
                node_loads[peer_id] = peer_node.load_score
        
        # Add own load
        node_loads[self.node_id] = getattr(self, 'current_load', 50)
        
        # Calculate load distribution
        total_load = sum(node_loads.values())
        avg_load = total_load / len(node_loads) if node_loads else 0
        
        # Find overloaded and underloaded nodes
        overloaded_nodes = {nid: load for nid, load in node_loads.items() if load > avg_load * 1.3}
        underloaded_nodes = {nid: load for nid, load in node_loads.items() if load < avg_load * 0.7}
        
        if overloaded_nodes and underloaded_nodes:
            # Propose load balancing
            proposal_data = {
                'overloaded_nodes': overloaded_nodes,
                'underloaded_nodes': underloaded_nodes,
                'target_avg_load': avg_load,
                'timestamp': time.time()
            }
            
            result = await self.propose_consensus_decision(
                "load_balancing", 
                proposal_data, 
                timeout_seconds=15.0
            )
            
            if result['status'] == 'approved':
                await self._execute_load_balancing(proposal_data)
                self.metrics['load_balancing_decisions'] += 1
    
    async def _execute_load_balancing(self, balancing_plan: Dict[str, Any]):
        """
        Execute approved load balancing plan
        
        Args:
            balancing_plan: Load balancing configuration
        """
        logger.info("Executing load balancing plan")
        
        # In real implementation, this would:
        # 1. Redistribute tasks from overloaded to underloaded nodes
        # 2. Update routing configurations
        # 3. Migrate data if necessary
        # 4. Update monitoring configurations
        
        # For simulation, just log the action
        overloaded = balancing_plan['overloaded_nodes']
        underloaded = balancing_plan['underloaded_nodes']
        
        for over_node, over_load in overloaded.items():
            for under_node, under_load in underloaded.items():
                transfer_amount = min(over_load - balancing_plan['target_avg_load'] * 1.1,
                                    balancing_plan['target_avg_load'] * 0.9 - under_load)
                
                if transfer_amount > 5:  # Only transfer if significant
                    logger.info(f"Load balancing: Transfer {transfer_amount:.1f} load from {over_node} to {under_node}")
    
    # ==========================================
    # HEARTBEAT AND FAILURE DETECTION
    # ==========================================
    
    async def _heartbeat_service(self):
        """Background service for heartbeat management"""
        while self.is_running:
            try:
                # Send heartbeats if leader
                if self.state == NodeState.LEADER:
                    await self._send_heartbeats()
                
                # Check for failed nodes
                await self._detect_failed_nodes()
                
                await asyncio.sleep(2.0)
                
            except Exception as e:
                logger.error(f"Error in heartbeat service: {e}")
    
    async def _detect_failed_nodes(self):
        """Detect failed nodes based on heartbeat timeouts"""
        current_time = time.time()
        newly_failed = []
        
        for peer_id, peer_node in self.peer_nodes.items():
            if peer_id not in self.failed_nodes:
                if current_time - peer_node.last_heartbeat > 15.0:  # 15 second timeout
                    self.failed_nodes.add(peer_id)
                    peer_node.is_alive = False
                    newly_failed.append(peer_id)
                    logger.warning(f"Node {peer_id} marked as failed")
        
        # If leader failed, start new election
        if self.leader_id in newly_failed and self.state == NodeState.FOLLOWER:
            logger.info("Leader failed, starting new election")
            await self._start_election()
    
    # ==========================================
    # PUBLIC API METHODS
    # ==========================================
    
    def add_peer_node(self, 
                     node_id: str, 
                     ip_address: str, 
                     port: int, 
                     capabilities: Dict[str, Any]):
        """Add a peer node to the collaboration network"""
        peer_node = EdgeNode(
            node_id=node_id,
            ip_address=ip_address,
            port=port,
            capabilities=capabilities,
            last_heartbeat=time.time()
        )
        
        with self.collaboration_lock:
            self.peer_nodes[node_id] = peer_node
        
        logger.info(f"Added peer node: {node_id}")
    
    def remove_peer_node(self, node_id: str):
        """Remove a peer node from the collaboration network"""
        with self.collaboration_lock:
            if node_id in self.peer_nodes:
                del self.peer_nodes[node_id]
            
            self.failed_nodes.discard(node_id)
        
        logger.info(f"Removed peer node: {node_id}")
    
    def get_collaboration_status(self) -> Dict[str, Any]:
        """Get comprehensive collaboration system status"""
        with self.collaboration_lock:
            return {
                'node_id': self.node_id,
                'state': self.state.value,
                'current_term': self.current_term,
                'leader_id': self.leader_id,
                'peer_nodes': len(self.peer_nodes),
                'failed_nodes': len(self.failed_nodes),
                'active_proposals': len(self.active_proposals),
                'held_locks': len(self.local_locks),
                'pending_lock_requests': len(self.lock_requests),
                'wait_for_graph_size': len(self.wait_for_graph),
                'metrics': self.metrics.copy(),
                'is_network_coordinator': self.state == NodeState.LEADER,
                'collaboration_health_score': self._calculate_collaboration_health()
            }
    
    def _calculate_collaboration_health(self) -> float:
        """Calculate overall collaboration system health score (0-100)"""
        health_factors = []
        
        # Consensus success rate
        health_factors.append(self.metrics['consensus_success_rate'] * 100)
        
        # Node availability
        total_nodes = len(self.peer_nodes) + 1
        available_nodes = total_nodes - len(self.failed_nodes)
        availability_score = (available_nodes / total_nodes) * 100 if total_nodes > 0 else 100
        health_factors.append(availability_score)
        
        # Deadlock resolution efficiency
        deadlocks_detected = self.metrics['deadlocks_detected']
        deadlocks_resolved = self.metrics['deadlocks_resolved']
        if deadlocks_detected > 0:
            deadlock_score = (deadlocks_resolved / deadlocks_detected) * 100
        else:
            deadlock_score = 100  # No deadlocks is good
        health_factors.append(deadlock_score)
        
        # Average consensus time (lower is better, normalize to 0-100)
        avg_time = self.metrics['average_consensus_time']
        time_score = max(0, 100 - avg_time * 2)  # 50 seconds = 0 score
        health_factors.append(time_score)
        
        return sum(health_factors) / len(health_factors) if health_factors else 0