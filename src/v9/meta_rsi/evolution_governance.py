"""Meta-RSI v9 — Evolution Governance Module (t_e78d3ecf)

Governs self-modification of RSI agents:
- Evolution proposals must pass peer review before deployment
- Rollback capability for every evolution step
- Audit trail for all self-modification attempts
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EvolutionStatus(Enum):
    PROPOSED = "proposed"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"


@dataclass
class EvolutionProposal:
    """A proposed self-modification to the agent."""
    proposal_id: str
    author: str
    description: str
    diff_hash: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: EvolutionStatus = EvolutionStatus.PROPOSED
    reviewers: list[str] = field(default_factory=list)
    approvals: list[str] = field(default_factory=list)
    rejections: list[str] = field(default_factory=list)
    parent_version: Optional[str] = None
    
    @property
    def is_approved(self) -> bool:
        return len(self.approvals) >= 2 and len(self.rejections) == 0
    
    @property
    def is_rejected(self) -> bool:
        return len(self.rejections) >= 1


@dataclass
class EvolutionRecord:
    """Immutable record of an evolution event."""
    record_id: str
    proposal_id: str
    action: str
    timestamp: str
    actor: str
    details: str = ""


class EvolutionGovernance:
    """Governs the evolution lifecycle of RSI agents."""
    
    def __init__(self, min_approvals: int = 2):
        self._proposals: dict[str, EvolutionProposal] = {}
        self._records: list[EvolutionRecord] = []
        self._min_approvals = min_approvals
    
    @property
    def proposals(self) -> dict[str, EvolutionProposal]:
        return dict(self._proposals)
    
    @property
    def records(self) -> list[EvolutionRecord]:
        return list(self._records)
    
    def propose(self, proposal_id: str, author: str, description: str, 
                diff: str, parent_version: Optional[str] = None) -> EvolutionProposal:
        """Submit a new evolution proposal."""
        if proposal_id in self._proposals:
            raise ValueError(f"Proposal {proposal_id} already exists")
        
        diff_hash = hashlib.sha256(diff.encode()).hexdigest()[:16]
        proposal = EvolutionProposal(
            proposal_id=proposal_id,
            author=author,
            description=description,
            diff_hash=diff_hash,
            parent_version=parent_version,
        )
        self._proposals[proposal_id] = proposal
        self._record(proposal_id, "PROPOSED", author, description)
        return proposal
    
    def assign_reviewer(self, proposal_id: str, reviewer: str) -> None:
        """Assign a reviewer to a proposal."""
        proposal = self._get_proposal(proposal_id)
        if reviewer not in proposal.reviewers:
            proposal.reviewers.append(reviewer)
            proposal.status = EvolutionStatus.REVIEWING
    
    def approve(self, proposal_id: str, reviewer: str) -> None:
        """Approve an evolution proposal."""
        proposal = self._get_proposal(proposal_id)
        if reviewer not in proposal.reviewers:
            raise ValueError(f"{reviewer} is not a reviewer for {proposal_id}")
        if reviewer not in proposal.approvals:
            proposal.approvals.append(reviewer)
            self._record(proposal_id, "APPROVED", reviewer, "")
            if len(proposal.approvals) >= self._min_approvals:
                proposal.status = EvolutionStatus.APPROVED
    
    def reject(self, proposal_id: str, reviewer: str, reason: str) -> None:
        """Reject an evolution proposal."""
        proposal = self._get_proposal(proposal_id)
        if reviewer not in proposal.reviewers:
            raise ValueError(f"{reviewer} is not a reviewer for {proposal_id}")
        if reviewer not in proposal.rejections:
            proposal.rejections.append(reviewer)
            proposal.status = EvolutionStatus.REJECTED
            self._record(proposal_id, "REJECTED", reviewer, reason)
    
    def deploy(self, proposal_id: str) -> None:
        """Deploy an approved evolution."""
        proposal = self._get_proposal(proposal_id)
        if proposal.status != EvolutionStatus.APPROVED:
            raise ValueError(f"Proposal {proposal_id} is not approved (status={proposal.status})")
        proposal.status = EvolutionStatus.DEPLOYED
        self._record(proposal_id, "DEPLOYED", "system", "")
    
    def rollback(self, proposal_id: str, reason: str) -> None:
        """Rollback a deployed evolution."""
        proposal = self._get_proposal(proposal_id)
        if proposal.status != EvolutionStatus.DEPLOYED:
            raise ValueError(f"Proposal {proposal_id} is not deployed (status={proposal.status})")
        proposal.status = EvolutionStatus.ROLLED_BACK
        self._record(proposal_id, "ROLLED_BACK", "system", reason)
    
    def get_status(self, proposal_id: str) -> EvolutionStatus:
        """Get the status of a proposal."""
        return self._get_proposal(proposal_id).status
    
    def get_audit_trail(self, proposal_id: str) -> list[EvolutionRecord]:
        """Get the audit trail for a proposal."""
        return [r for r in self._records if r.proposal_id == proposal_id]
    
    def _get_proposal(self, proposal_id: str) -> EvolutionProposal:
        if proposal_id not in self._proposals:
            raise KeyError(f"Proposal {proposal_id} not found")
        return self._proposal(proposal_id)
    
    def _record(self, proposal_id: str, action: str, actor: str, details: str) -> None:
        record = EvolutionRecord(
            record_id=f"rec-{len(self._records)+1:04d}",
            proposal_id=proposal_id,
            action=action,
            timestamp=datetime.utcnow().isoformat(),
            actor=actor,
            details=details,
        )
        self._records.append(record)
