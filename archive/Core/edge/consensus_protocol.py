"""
Consensus Protocol Module

Implements consensus algorithms for distributed decision making in the
EDGE-QI edge computing network. Enables coordinated decisions across
multiple edge devices for queue management and traffic optimization.
"""

import asyncio
import time
import json
import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import random

from .edge_communication import EdgeMessage, MessageType, EdgeCommunication

logger = logging.getLogger(__name__)

class ConsensusType(Enum):
    """Types of consensus algorithms supported"""
    RAFT = "raft"
    PBFT = "pbft"  # Practical Byzantine Fault Tolerance
    SIMPLE_MAJORITY = "simple_majority"
    WEIGHTED_CONSENSUS = "weighted_consensus"

@dataclass
class ConsensusProposal:
    """A proposal for consensus voting"""
    proposal_id: str
    proposer_id: str
    proposal_type: str  # e.g., "traffic_signal_timing", "queue_priority"
    proposal_data: Dict[str, Any]
    timestamp: float
    deadline: float  # When voting closes
    priority: int = 1

@dataclass
class ConsensusVote:
    """A vote in the consensus process"""
    proposal_id: str
    voter_id: str
    vote: bool  # True = agree, False = disagree
    timestamp: float
    weight: float = 1.0
    reasoning: Optional[str] = None

@dataclass
class ConsensusResult:
    """Result of a consensus decision"""
    proposal_id: str
    decision: bool  # True = accepted, False = rejected
    vote_count: int
    votes_for: int
    votes_against: int
    total_weight: float
    weight_for: float
    weight_against: float
    confidence: float  # 0.0 to 1.0
    participants: List[str]
    duration: float  # Time taken to reach consensus

class ConsensusProtocol:
    """
    Distributed consensus protocol for edge device coordination.
    
    Features:
    - Multiple consensus algorithms (Raft, PBFT, Simple Majority)
    - Weighted voting based on edge capabilities
    - Byzantine fault tolerance options
    - Timeout handling and partial consensus
    - Audit trail and decision logging
    """
    
    def __init__(self, 
                 edge_id: str,
                 communication: EdgeCommunication,
                 consensus_type: ConsensusType = ConsensusType.SIMPLE_MAJORITY,
                 vote_timeout: float = 30.0):
        self.edge_id = edge_id
        self.communication = communication
        self.consensus_type = consensus_type
        self.vote_timeout = vote_timeout
        
        # Consensus state
        self.active_proposals: Dict[str, ConsensusProposal] = {}
        self.proposal_votes: Dict[str, List[ConsensusVote]] = {}
        self.consensus_history: List[ConsensusResult] = []
        self.edge_weights: Dict[str, float] = {}
        
        # RAFT-specific state
        self.current_term = 0
        self.voted_for = None
        self.is_leader = False
        self.last_heartbeat = 0
        
        # Statistics
        self.stats = {
            'proposals_initiated': 0,
            'proposals_participated': 0,
            'consensus_reached': 0,
            'consensus_failed': 0,
            'average_consensus_time': 0.0
        }
        
        # Register message handlers
        self.communication.register_handler(
            MessageType.CONSENSUS_REQUEST, 
            self._handle_consensus_request
        )
        self.communication.register_handler(
            MessageType.CONSENSUS_RESPONSE, 
            self._handle_consensus_response
        )
        
        logger.info(f"Consensus protocol initialized for {edge_id} using {consensus_type.value}")
    
    async def propose_decision(self, 
                              proposal_type: str,
                              proposal_data: Dict[str, Any],
                              timeout: Optional[float] = None,
                              priority: int = 1) -> ConsensusResult:
        """
        Propose a decision for consensus voting.
        
        Args:
            proposal_type: Type of decision (e.g., "signal_timing", "queue_priority")
            proposal_data: Data for the proposal
            timeout: Voting timeout (uses default if None)
            priority: Proposal priority (1-10)
        
        Returns:
            ConsensusResult: The result of the consensus process
        """
        proposal_id = f"{self.edge_id}_{proposal_type}_{int(time.time())}"
        current_time = time.time()
        deadline = current_time + (timeout or self.vote_timeout)
        
        proposal = ConsensusProposal(
            proposal_id=proposal_id,
            proposer_id=self.edge_id,
            proposal_type=proposal_type,
            proposal_data=proposal_data,
            timestamp=current_time,
            deadline=deadline,
            priority=priority
        )
        
        # Store proposal
        self.active_proposals[proposal_id] = proposal
        self.proposal_votes[proposal_id] = []
        
        # Broadcast proposal to all connected edges
        request_message = EdgeMessage(
            message_id=f"consensus_req_{proposal_id}",
            sender_id=self.edge_id,
            receiver_id="broadcast",
            message_type=MessageType.CONSENSUS_REQUEST,
            timestamp=current_time,
            data={
                'proposal': {
                    'proposal_id': proposal_id,
                    'proposer_id': self.edge_id,
                    'proposal_type': proposal_type,
                    'proposal_data': proposal_data,
                    'deadline': deadline,
                    'priority': priority
                },
                'consensus_type': self.consensus_type.value
            },
            priority=priority + 2
        )
        
        await self.communication.send_message(request_message)
        
        # Vote on our own proposal
        own_vote = self._evaluate_proposal(proposal)
        await self._cast_vote(proposal_id, own_vote, "Self-evaluation")
        
        self.stats['proposals_initiated'] += 1
        logger.info(f"Proposed {proposal_type} for consensus: {proposal_id}")
        
        # Wait for consensus or timeout
        return await self._wait_for_consensus(proposal_id)
    
    async def _handle_consensus_request(self, message: EdgeMessage):
        """Handle incoming consensus requests"""
        try:
            proposal_data = message.data['proposal']
            proposal_id = proposal_data['proposal_id']
            proposer_id = proposal_data['proposer_id']
            
            # Check if we already have this proposal
            if proposal_id in self.active_proposals:
                return
            
            # Create proposal object
            proposal = ConsensusProposal(
                proposal_id=proposal_id,
                proposer_id=proposer_id,
                proposal_type=proposal_data['proposal_type'],
                proposal_data=proposal_data['proposal_data'],
                timestamp=proposal_data.get('timestamp', time.time()),
                deadline=proposal_data['deadline'],
                priority=proposal_data.get('priority', 1)
            )
            
            # Check if proposal is still valid
            if time.time() > proposal.deadline:
                logger.warning(f"Received expired proposal {proposal_id}")
                return
            
            # Store proposal
            self.active_proposals[proposal_id] = proposal
            self.proposal_votes[proposal_id] = []
            
            # Evaluate and vote
            vote_decision = self._evaluate_proposal(proposal)
            reasoning = self._get_vote_reasoning(proposal, vote_decision)
            
            await self._cast_vote(proposal_id, vote_decision, reasoning)
            
            # Send response to proposer
            response_message = EdgeMessage(
                message_id=f"consensus_resp_{proposal_id}_{self.edge_id}",
                sender_id=self.edge_id,
                receiver_id=proposer_id,
                message_type=MessageType.CONSENSUS_RESPONSE,
                timestamp=time.time(),
                data={
                    'proposal_id': proposal_id,
                    'vote': vote_decision,
                    'weight': self._get_edge_weight(self.edge_id),
                    'reasoning': reasoning
                }
            )
            
            await self.communication.send_message(response_message)
            self.stats['proposals_participated'] += 1
            
        except Exception as e:
            logger.error(f"Error handling consensus request: {e}")
    
    async def _handle_consensus_response(self, message: EdgeMessage):
        """Handle consensus response votes"""
        try:
            proposal_id = message.data['proposal_id']
            voter_id = message.sender_id
            vote_decision = message.data['vote']
            weight = message.data.get('weight', 1.0)
            reasoning = message.data.get('reasoning', '')
            
            if proposal_id not in self.active_proposals:
                logger.warning(f"Received vote for unknown proposal {proposal_id}")
                return
            
            # Record the vote
            vote = ConsensusVote(
                proposal_id=proposal_id,
                voter_id=voter_id,
                vote=vote_decision,
                weight=weight,
                timestamp=time.time(),
                reasoning=reasoning
            )
            
            # Check for duplicate votes
            existing_votes = [v for v in self.proposal_votes[proposal_id] if v.voter_id == voter_id]
            if existing_votes:
                logger.warning(f"Duplicate vote from {voter_id} for {proposal_id}")
                return
            
            self.proposal_votes[proposal_id].append(vote)
            logger.info(f"Received vote from {voter_id} for {proposal_id}: {vote_decision}")
            
        except Exception as e:
            logger.error(f"Error handling consensus response: {e}")
    
    def _evaluate_proposal(self, proposal: ConsensusProposal) -> bool:
        """
        Evaluate a proposal and decide how to vote.
        This is where edge-specific logic for decision making goes.
        """
        proposal_type = proposal.proposal_type
        data = proposal.proposal_data
        
        # Implement specific evaluation logic based on proposal type
        if proposal_type == "traffic_signal_timing":
            return self._evaluate_signal_timing_proposal(data)
        elif proposal_type == "queue_priority":
            return self._evaluate_queue_priority_proposal(data)
        elif proposal_type == "emergency_protocol":
            return self._evaluate_emergency_proposal(data)
        elif proposal_type == "load_balancing":
            return self._evaluate_load_balancing_proposal(data)
        else:
            # Default evaluation based on proposal quality metrics
            return self._default_proposal_evaluation(data)
    
    def _evaluate_signal_timing_proposal(self, data: Dict[str, Any]) -> bool:
        """Evaluate traffic signal timing proposals"""
        # Check if proposal improves traffic flow
        proposed_timing = data.get('timing', {})
        current_load = data.get('traffic_load', 0.5)
        expected_improvement = data.get('expected_improvement', 0.0)
        
        # Vote yes if improvement is significant and load is high
        return current_load > 0.6 and expected_improvement > 0.1
    
    def _evaluate_queue_priority_proposal(self, data: Dict[str, Any]) -> bool:
        """Evaluate queue priority adjustment proposals"""
        priority_change = data.get('priority_change', 0)
        queue_length = data.get('queue_length', 0)
        wait_time = data.get('average_wait_time', 0)
        
        # Vote yes if queues are long and wait times are high
        return queue_length > 10 and wait_time > 300  # 5 minutes
    
    def _evaluate_emergency_proposal(self, data: Dict[str, Any]) -> bool:
        """Evaluate emergency protocol proposals"""
        emergency_level = data.get('emergency_level', 1)
        confidence = data.get('confidence', 0.0)
        
        # Vote yes for high-confidence emergency situations
        return emergency_level >= 3 and confidence > 0.8
    
    def _evaluate_load_balancing_proposal(self, data: Dict[str, Any]) -> bool:
        """Evaluate load balancing proposals"""
        current_load = self.communication._get_current_load()
        target_load = data.get('target_load', 0.5)
        
        # Vote yes if our load is high and proposal suggests redistribution
        return current_load > 0.8 and target_load < current_load
    
    def _default_proposal_evaluation(self, data: Dict[str, Any]) -> bool:
        """Default proposal evaluation"""
        # Conservative approach: vote yes if confidence is high
        confidence = data.get('confidence', 0.0)
        return confidence > 0.7
    
    def _get_vote_reasoning(self, proposal: ConsensusProposal, vote: bool) -> str:
        """Generate reasoning for vote decision"""
        if vote:
            return f"Supporting {proposal.proposal_type} due to positive evaluation"
        else:
            return f"Opposing {proposal.proposal_type} due to insufficient confidence"
    
    async def _cast_vote(self, proposal_id: str, vote: bool, reasoning: str):
        """Cast a vote for a proposal"""
        vote_obj = ConsensusVote(
            proposal_id=proposal_id,
            voter_id=self.edge_id,
            vote=vote,
            weight=self._get_edge_weight(self.edge_id),
            timestamp=time.time(),
            reasoning=reasoning
        )
        
        if proposal_id not in self.proposal_votes:
            self.proposal_votes[proposal_id] = []
        
        self.proposal_votes[proposal_id].append(vote_obj)
        logger.info(f"Cast vote for {proposal_id}: {vote} ({reasoning})")
    
    def _get_edge_weight(self, edge_id: str) -> float:
        """Get voting weight for an edge device"""
        if edge_id in self.edge_weights:
            return self.edge_weights[edge_id]
        
        # Default weight calculation based on edge capabilities
        if edge_id == self.edge_id:
            # Our own weight based on capabilities
            return 1.0
        else:
            # Other edges get equal weight by default
            return 1.0
    
    def set_edge_weight(self, edge_id: str, weight: float):
        """Set voting weight for an edge device"""
        self.edge_weights[edge_id] = max(0.1, min(weight, 5.0))  # Clamp between 0.1 and 5.0
        logger.info(f"Set voting weight for {edge_id}: {weight}")
    
    async def _wait_for_consensus(self, proposal_id: str) -> ConsensusResult:
        """Wait for consensus to be reached or timeout"""
        proposal = self.active_proposals[proposal_id]
        start_time = time.time()
        
        while time.time() < proposal.deadline:
            # Check if we have enough votes
            result = self._calculate_consensus_result(proposal_id)
            if result:
                # Consensus reached
                duration = time.time() - start_time
                result.duration = duration
                
                # Clean up
                del self.active_proposals[proposal_id]
                del self.proposal_votes[proposal_id]
                
                # Update statistics
                if result.decision:
                    self.stats['consensus_reached'] += 1
                else:
                    self.stats['consensus_failed'] += 1
                
                # Update average consensus time
                current_avg = self.stats['average_consensus_time']
                count = self.stats['consensus_reached'] + self.stats['consensus_failed']
                self.stats['average_consensus_time'] = (current_avg * (count - 1) + duration) / count
                
                # Store in history
                self.consensus_history.append(result)
                
                logger.info(f"Consensus reached for {proposal_id}: {result.decision} "
                           f"({result.votes_for}/{result.vote_count} votes, {duration:.1f}s)")
                
                return result
            
            # Wait a bit before checking again
            await asyncio.sleep(1.0)
        
        # Timeout reached - calculate final result
        result = self._calculate_consensus_result(proposal_id, final=True)
        if not result:
            # Create a failed consensus result
            votes = self.proposal_votes.get(proposal_id, [])
            result = ConsensusResult(
                proposal_id=proposal_id,
                decision=False,
                vote_count=len(votes),
                votes_for=sum(1 for v in votes if v.vote),
                votes_against=sum(1 for v in votes if not v.vote),
                total_weight=sum(v.weight for v in votes),
                weight_for=sum(v.weight for v in votes if v.vote),
                weight_against=sum(v.weight for v in votes if not v.vote),
                confidence=0.0,
                participants=[v.voter_id for v in votes],
                duration=time.time() - start_time
            )
        
        # Clean up
        if proposal_id in self.active_proposals:
            del self.active_proposals[proposal_id]
        if proposal_id in self.proposal_votes:
            del self.proposal_votes[proposal_id]
        
        self.stats['consensus_failed'] += 1
        self.consensus_history.append(result)
        
        logger.warning(f"Consensus timeout for {proposal_id}: {result.decision}")
        return result
    
    def _calculate_consensus_result(self, proposal_id: str, final: bool = False) -> Optional[ConsensusResult]:
        """Calculate consensus result based on current votes"""
        if proposal_id not in self.proposal_votes:
            return None
        
        votes = self.proposal_votes[proposal_id]
        if not votes:
            return None
        
        # Count votes and weights
        vote_count = len(votes)
        votes_for = sum(1 for v in votes if v.vote)
        votes_against = vote_count - votes_for
        
        total_weight = sum(v.weight for v in votes)
        weight_for = sum(v.weight for v in votes if v.vote)
        weight_against = total_weight - weight_for
        
        participants = [v.voter_id for v in votes]
        
        # Apply consensus algorithm
        decision = False
        confidence = 0.0
        
        if self.consensus_type == ConsensusType.SIMPLE_MAJORITY:
            decision = votes_for > votes_against
            confidence = abs(votes_for - votes_against) / vote_count
            
        elif self.consensus_type == ConsensusType.WEIGHTED_CONSENSUS:
            decision = weight_for > weight_against
            confidence = abs(weight_for - weight_against) / total_weight
            
        # For final results or if we have enough participants
        connected_edges = len(self.communication.connected_edges) + 1  # +1 for self
        min_participants = max(2, connected_edges // 2 + 1)  # Majority of connected edges
        
        if final or vote_count >= min_participants:
            return ConsensusResult(
                proposal_id=proposal_id,
                decision=decision,
                vote_count=vote_count,
                votes_for=votes_for,
                votes_against=votes_against,
                total_weight=total_weight,
                weight_for=weight_for,
                weight_against=weight_against,
                confidence=confidence,
                participants=participants,
                duration=0.0  # Will be set by caller
            )
        
        return None
    
    def get_consensus_history(self, limit: int = 10) -> List[ConsensusResult]:
        """Get recent consensus history"""
        return self.consensus_history[-limit:]
    
    def get_active_proposals(self) -> List[ConsensusProposal]:
        """Get currently active proposals"""
        return list(self.active_proposals.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get consensus statistics"""
        stats = self.stats.copy()
        stats['active_proposals'] = len(self.active_proposals)
        stats['consensus_success_rate'] = (
            stats['consensus_reached'] / 
            max(1, stats['consensus_reached'] + stats['consensus_failed'])
        )
        return stats

# Utility functions for common consensus scenarios

async def propose_traffic_signal_change(consensus: ConsensusProtocol,
                                       intersection_id: str,
                                       new_timing: Dict[str, float],
                                       traffic_load: float,
                                       expected_improvement: float) -> ConsensusResult:
    """Propose a traffic signal timing change"""
    proposal_data = {
        'intersection_id': intersection_id,
        'timing': new_timing,
        'traffic_load': traffic_load,
        'expected_improvement': expected_improvement,
        'confidence': min(expected_improvement * 2, 1.0)
    }
    
    return await consensus.propose_decision(
        "traffic_signal_timing",
        proposal_data,
        timeout=20.0,  # Quick decision for traffic
        priority=4
    )

async def propose_emergency_protocol(consensus: ConsensusProtocol,
                                   emergency_type: str,
                                   location: Tuple[float, float],
                                   severity: int,
                                   confidence: float) -> ConsensusResult:
    """Propose activating emergency protocol"""
    proposal_data = {
        'emergency_type': emergency_type,
        'location': location,
        'emergency_level': severity,
        'confidence': confidence,
        'timestamp': time.time()
    }
    
    return await consensus.propose_decision(
        "emergency_protocol",
        proposal_data,
        timeout=10.0,  # Very quick for emergencies
        priority=10
    )

async def propose_load_balancing(consensus: ConsensusProtocol,
                               current_load: float,
                               target_distribution: Dict[str, float]) -> ConsensusResult:
    """Propose load balancing across edge devices"""
    proposal_data = {
        'current_load': current_load,
        'target_distribution': target_distribution,
        'target_load': sum(target_distribution.values()) / len(target_distribution)
    }
    
    return await consensus.propose_decision(
        "load_balancing",
        proposal_data,
        timeout=30.0,
        priority=3
    )