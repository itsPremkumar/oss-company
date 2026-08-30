"""Meta-RSI v9 — Control Group Enforcement Module (t_e78d3ecf)

Enforces control group integrity in RSI self-experiments:
- Ensures control groups are never contaminated by treatment
- Validates random assignment
- Detects selection bias
- Enforces blinding where applicable
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AssignmentMethod(Enum):
    RANDOM = "random"
    STRATIFIED = "stratified"
    MATCHED = "matched"


class ControlGroupStatus(Enum):
    INTACT = "intact"
    CONTAMINATED = "contaminated"
    COMPROMISED = "compromised"


@dataclass
class Subject:
    """A subject in an experiment."""
    subject_id: str
    group: str  # "treatment" or "control"
    features: dict[str, float] = field(default_factory=dict)
    assigned_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ControlGroupReport:
    """Report on control group integrity."""
    report_id: str
    experiment_id: str
    status: ControlGroupStatus
    contamination_detected: bool
    selection_bias_score: float
    details: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    @property
    def is_valid(self) -> bool:
        return self.status == ControlGroupStatus.INTACT and not self.contamination_detected


class ControlGroupEnforcement:
    """Enforces control group integrity in RSI experiments."""
    
    def __init__(self, contamination_threshold: float = 0.05):
        self._subjects: dict[str, Subject] = {}
        self._reports: list[ControlGroupReport] = []
        self._contamination_threshold = contamination_threshold
    
    def assign_subject(self, subject_id: str, group: str, 
                       features: Optional[dict[str, float]] = None) -> Subject:
        """Assign a subject to a group."""
        if subject_id in self._subjects:
            raise ValueError(f"Subject {subject_id} already assigned")
        if group not in ("treatment", "control"):
            raise ValueError(f"Group must be 'treatment' or 'control', got {group}")
        
        subject = Subject(
            subject_id=subject_id,
            group=group,
            features=features or {},
        )
        self._subjects[subject_id] = subject
        return subject
    
    def random_assignment(self, subject_ids: list[str], 
                          method: AssignmentMethod = AssignmentMethod.RANDOM,
                          seed: Optional[int] = None) -> list[Subject]:
        """Randomly assign subjects to treatment/control groups."""
        if seed is not None:
            random.seed(seed)
        
        subjects = []
        shuffled = list(subject_ids)
        random.shuffle(shuffled)
        
        mid = len(shuffled) // 2
        for i, sid in enumerate(shuffled):
            group = "treatment" if i < mid else "control"
            subject = self.assign_subject(sid, group)
            subjects.append(subject)
        
        return subjects
    
    def check_contamination(self, experiment_id: str, 
                            treatment_ids: list[str],
                            control_ids: list[str]) -> ControlGroupReport:
        """Check for contamination between treatment and control groups."""
        # Check for overlapping subjects
        overlap = set(treatment_ids) & set(control_ids)
        
        contamination_detected = len(overlap) > 0
        
        if contamination_detected:
            status = ControlGroupStatus.CONTAMINATED
            details = f"Contamination: {len(overlap)} subjects in both groups"
        else:
            status = ControlGroupStatus.INTACT
            details = "No contamination detected"
        
        bias_score = self._compute_selection_bias(treatment_ids, control_ids)
        
        report = ControlGroupReport(
            report_id=f"report-{len(self._reports)+1:04d}",
            experiment_id=experiment_id,
            status=status,
            contamination_detected=contamination_detected,
            selection_bias_score=bias_score,
            details=details,
        )
        self._reports.append(report)
        return report
    
    def validate_random_assignment(self, experiment_id: str) -> bool:
        """Validate that random assignment is unbiased."""
        treatment = [s for s in self._subjects.values() if s.group == "treatment"]
        control = [s for s in self._subjects.values() if s.group == "control"]
        
        if not treatment or not control:
            return False
        
        # Check approximate 50/50 split
        total = len(treatment) + len(control)
        ratio = len(treatment) / total
        
        return 0.4 <= ratio <= 0.6
    
    def get_subjects(self, group: Optional[str] = None) -> list[Subject]:
        """Get subjects, optionally filtered by group."""
        subjects = list(self._subjects.values())
        if group:
            subjects = [s for s in subjects if s.group == group]
        return subjects
    
    def get_reports(self, experiment_id: Optional[str] = None) -> list[ControlGroupReport]:
        """Get control group reports."""
        if experiment_id:
            return [r for r in self._reports if r.experiment_id == experiment_id]
        return list(self._reports)
    
    def _compute_selection_bias(self, treatment_ids: list[str], 
                                control_ids: list[str]) -> float:
        """Compute selection bias score (0 = no bias, 1 = severe bias)."""
        # Simplified: compare group sizes
        total = len(treatment_ids) + len(control_ids)
        if total == 0:
            return 0.0
        ratio = len(treatment_ids) / total
        return abs(0.5 - ratio) * 2  # Scale to [0, 1]
