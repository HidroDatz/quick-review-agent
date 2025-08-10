from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON


class User(SQLModel, table=True):
    gitlab_user_id: int = Field(primary_key=True)
    username: str
    name: str
    email: str
    findings: List["Finding"] = Relationship(back_populates="resolved_by_user")


class MergeRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int
    mr_iid: int
    title: str
    author_id: int | None = Field(default=None, foreign_key="user.gitlab_user_id")
    state: str
    created_at: datetime
    updated_at: datetime
    snapshots: List["MRSnapshot"] = Relationship(back_populates="mr")


class MRSnapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    mr_id: int = Field(foreign_key="mergerequest.id")
    head_sha: str
    base_sha: str
    description_hash: str
    languages: List[str] = Field(sa_column=Column(JSON))
    risk_level: str
    created_at: datetime
    mr: MergeRequest = Relationship(back_populates="snapshots")
    findings: List["Finding"] = Relationship(back_populates="snapshot")


class Finding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    snapshot_id: int = Field(foreign_key="mrsnapshot.id")
    file: str
    start_line: int
    end_line: int
    severity: str
    category: str
    rule_id: str
    rule_version: str
    title: str
    rationale: str
    recommendation: str
    patch: str
    model_name: str
    confidence: float
    status: str
    first_seen_at: datetime
    resolved_at: datetime | None = None
    resolved_by_user_id: int | None = Field(default=None, foreign_key="user.gitlab_user_id")
    evidence_excerpt: str | None = None
    dedupe_key: str
    user_issue_key: str
    snapshot: MRSnapshot = Relationship(back_populates="findings")
    resolved_by_user: Optional[User] = Relationship(back_populates="findings")


class UserIssueCatalog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.gitlab_user_id")
    issue_key: str
    title: str
    description: str
    category: str
    last_seen_at: datetime
    total_occurrences: int
    open_occurrences: int


class FindingToUserIssue(SQLModel, table=True):
    finding_id: int = Field(foreign_key="finding.id", primary_key=True)
    user_issue_id: int = Field(foreign_key="userissuecatalog.id", primary_key=True)


class MRMetrics(SQLModel, table=True):
    mr_id: int = Field(foreign_key="mergerequest.id", primary_key=True)
    snapshot_id: int = Field(foreign_key="mrsnapshot.id", primary_key=True)
    counts_by_severity: dict = Field(sa_column=Column(JSON))
    counts_by_category: dict = Field(sa_column=Column(JSON))
    open_count: int
    resolved_count: int
    avg_time_to_resolve_hours: float
    created_at: datetime


class UserMetricsDaily(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.gitlab_user_id", primary_key=True)
    date: datetime = Field(primary_key=True)
    introduced_findings: int
    resolved_findings: int
    median_ttr_hours: float
    top_issue_keys: dict = Field(sa_column=Column(JSON))
