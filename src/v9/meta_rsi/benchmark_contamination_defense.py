"""Meta-RSI v9 — Benchmark Contamination Defense Module (t_e78d3ecf)

Defends against benchmark contamination in RSI training:
- Detects if training data has leaked into benchmarks
- Enforces strict data separation
- Validates benchmark integrity before evaluation
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ContaminationLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DataSegment:
    """A segment of data with provenance tracking."""
    segment_id: str
    source: str
    content_hash: str
    created_at: str
    tags: list[str] = field(default_factory=list)


@dataclass
class ContaminationReport:
    """Report of contamination detection."""
    report_id: str
    benchmark_id: str
    contamination_level: ContaminationLevel
    matches: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: str = ""
    
    @property
    def is_clean(self) -> bool:
        return self.contamination_level == ContaminationLevel.NONE
    
    @property
    def is_contaminated(self) -> bool:
        return self.contamination_level in (
            ContaminationLevel.HIGH, ContaminationLevel.CRITICAL
        )


class BenchmarkContaminationDefense:
    """Defends against benchmark contamination in RSI evaluation."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self._training_data: dict[str, DataSegment] = {}
        self._benchmarks: dict[str, DataSegment] = {}
        self._reports: list[ContaminationReport] = []
        self._similarity_threshold = similarity_threshold
    
    def register_training_data(self, segment_id: str, source: str, 
                                content: str, tags: Optional[list[str]] = None) -> DataSegment:
        """Register a training data segment."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        segment = DataSegment(
            segment_id=segment_id,
            source=source,
            content_hash=content_hash,
            created_at=datetime.utcnow().isoformat(),
            tags=tags or [],
        )
        self._training_data[segment_id] = segment
        return segment
    
    def register_benchmark(self, benchmark_id: str, source: str, 
                           content: str, tags: Optional[list[str]] = None) -> DataSegment:
        """Register a benchmark data segment."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        segment = DataSegment(
            segment_id=benchmark_id,
            source=source,
            content_hash=content_hash,
            created_at=datetime.utcnow().isoformat(),
            tags=tags or [],
        )
        self._benchmarks[benchmark_id] = segment
        return segment
    
    def check_contamination(self, benchmark_id: str) -> ContaminationReport:
        """Check a benchmark for contamination from training data."""
        if benchmark_id not in self._benchmarks:
            raise KeyError(f"Benchmark {benchmark_id} not found")
        
        benchmark = self._benchmarks[benchmark_id]
        matches = []
        
        for train_id, train_segment in self._training_data.items():
            similarity = self._compute_similarity(benchmark.content_hash, train_segment.content_hash)
            if similarity >= self._similarity_threshold:
                matches.append(train_id)
        
        level = self._classify_contamination(len(matches))
        report = ContaminationReport(
            report_id=f"report-{len(self._reports)+1:04d}",
            benchmark_id=benchmark_id,
            contamination_level=level,
            matches=matches,
            details=f"Found {len(matches)} matching training segments",
        )
        self._reports.append(report)
        return report
    
    def validate_benchmark_integrity(self, benchmark_id: str) -> bool:
        """Validate a benchmark is safe to use (not contaminated)."""
        report = self.check_contamination(benchmark_id)
        return not report.is_contaminated
    
    def get_reports(self, benchmark_id: Optional[str] = None) -> list[ContaminationReport]:
        """Get contamination reports, optionally filtered by benchmark."""
        if benchmark_id:
            return [r for r in self._reports if r.benchmark_id == benchmark_id]
        return list(self._reports)
    
    def _compute_similarity(self, hash_a: str, hash_b: str) -> float:
        """Compute similarity between two content hashes (simplified)."""
        if hash_a == hash_b:
            return 1.0
        # Simplified: count matching hex chars as proxy
        matches = sum(1 for a, b in zip(hash_a, hash_b) if a == b)
        return matches / max(len(hash_a), len(hash_b))
    
    def _classify_contamination(self, match_count: int) -> ContaminationLevel:
        """Classify contamination level based on match count."""
        if match_count == 0:
            return ContaminationLevel.NONE
        elif match_count <= 2:
            return ContaminationLevel.LOW
        elif match_count <= 5:
            return ContaminationLevel.MEDIUM
        elif match_count <= 10:
            return ContaminationLevel.HIGH
        else:
            return ContaminationLevel.CRITICAL
