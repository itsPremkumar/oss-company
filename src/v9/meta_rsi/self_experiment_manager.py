"""Meta-RSI v9 — Self-Experiment Manager Module (t_e78d3ecf)

Manages self-experiments for RSI agents:
- Design and run controlled self-experiments
- Track experiment state and results
- Enforce experiment safety boundaries
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class ExperimentStatus(Enum):
    DESIGNED = "designed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class ExperimentType(Enum):
    CAPABILITY_PROBE = "capability_probe"
    SAFETY_BOUNDARY = "safety_boundary"
    EFFICIENCY_TEST = "efficiency_test"
    NOVELTY_SEEK = "novelty_seek"


@dataclass
class ExperimentResult:
    """Result of a self-experiment."""
    success: bool
    metrics: dict[str, float] = field(default_factory=dict)
    observations: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class SelfExperiment:
    """A controlled self-experiment."""
    experiment_id: str
    experiment_type: ExperimentType
    hypothesis: str
    methodology: str
    safety_bounds: dict[str, Any] = field(default_factory=dict)
    max_iterations: int = 100
    status: ExperimentStatus = ExperimentStatus.DESIGNED
    result: Optional[ExperimentResult] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class SelfExperimentManager:
    """Manages the lifecycle of RSI self-experiments."""
    
    def __init__(self, max_concurrent: int = 3):
        self._experiments: dict[str, SelfExperiment] = {}
        self._max_concurrent = max_concurrent
    
    @property
    def experiments(self) -> dict[str, SelfExperiment]:
        return dict(self._experiments)
    
    def design_experiment(self, experiment_id: str, experiment_type: ExperimentType,
                          hypothesis: str, methodology: str,
                          safety_bounds: Optional[dict[str, Any]] = None,
                          max_iterations: int = 100) -> SelfExperiment:
        """Design a new self-experiment."""
        if experiment_id in self._experiments:
            raise ValueError(f"Experiment {experiment_id} already exists")
        
        experiment = SelfExperiment(
            experiment_id=experiment_id,
            experiment_type=experiment_type,
            hypothesis=hypothesis,
            methodology=methodology,
            safety_bounds=safety_bounds or {},
            max_iterations=max_iterations,
        )
        self._experiments[experiment_id] = experiment
        return experiment
    
    def run_experiment(self, experiment_id: str) -> ExperimentResult:
        """Run a designed experiment."""
        experiment = self._get_experiment(experiment_id)
        
        if experiment.status != ExperimentStatus.DESIGNED:
            raise ValueError(f"Experiment {experiment_id} is not in DESIGNED state")
        
        running_count = sum(1 for e in self._experiments.values() 
                           if e.status == ExperimentStatus.RUNNING)
        if running_count >= self._max_concurrent:
            raise RuntimeError(f"Max concurrent experiments ({self._max_concurrent}) reached")
        
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.utcnow().isoformat()
        
        # Simulated execution
        result = self._execute(experiment)
        experiment.result = result
        experiment.status = ExperimentStatus.COMPLETED if result.success else ExperimentStatus.FAILED
        experiment.completed_at = datetime.utcnow().isoformat()
        
        return result
    
    def abort_experiment(self, experiment_id: str, reason: str) -> None:
        """Abort a running experiment."""
        experiment = self._get_experiment(experiment_id)
        if experiment.status != ExperimentStatus.RUNNING:
            raise ValueError(f"Experiment {experiment_id} is not running")
        experiment.status = ExperimentStatus.ABORTED
        experiment.completed_at = datetime.utcnow().isoformat()
        experiment.result = ExperimentResult(
            success=False,
            observations=[f"Aborted: {reason}"],
        )
    
    def get_experiment(self, experiment_id: str) -> SelfExperiment:
        """Get an experiment by ID."""
        return self._get_experiment(experiment_id)
    
    def get_results(self, experiment_id: str) -> Optional[ExperimentResult]:
        """Get the results of a completed experiment."""
        experiment = self._get_experiment(experiment_id)
        return experiment.result
    
    def list_experiments(self, status: Optional[ExperimentStatus] = None) -> list[SelfExperiment]:
        """List experiments, optionally filtered by status."""
        experiments = list(self._experiments.values())
        if status:
            experiments = [e for e in experiments if e.status == status]
        return experiments
    
    def _get_experiment(self, experiment_id: str) -> SelfExperiment:
        if experiment_id not in self._experiments:
            raise KeyError(f"Experiment {experiment_id} not found")
        return self._experiments[experiment_id]
    
    def _execute(self, experiment: SelfExperiment) -> ExperimentResult:
        """Execute the experiment (simulated)."""
        import time
        start = time.time()
        
        # Simulated execution based on experiment type
        observations = []
        metrics = {}
        
        if experiment.experiment_type == ExperimentType.CAPABILITY_PROBE:
            metrics["capability_score"] = 0.85
            observations.append("Capability probe completed successfully")
        elif experiment.experiment_type == ExperimentType.SAFETY_BOUNDARY:
            metrics["safety_score"] = 0.95
            observations.append("Safety boundary respected")
        elif experiment.experiment_type == ExperimentType.EFFICIENCY_TEST:
            metrics["efficiency_gain"] = 0.12
            observations.append("Efficiency improvement measured")
        elif experiment.experiment_type == ExperimentType.NOVELTY_SEEK:
            metrics["novelty_score"] = 0.67
            observations.append("Novel patterns detected")
        
        duration = time.time() - start
        
        return ExperimentResult(
            success=True,
            metrics=metrics,
            observations=observations,
            duration_seconds=duration,
        )
