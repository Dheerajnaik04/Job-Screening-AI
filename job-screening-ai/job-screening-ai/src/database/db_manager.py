from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import Base, Job, Candidate, Match, Interview

# Create async engine
engine = create_async_engine(
    "sqlite+aiosqlite:///job_screening.db",
    echo=True
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initialize the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class DatabaseManager:
    @staticmethod
    async def get_session() -> AsyncSession:
        """Get a database session."""
        async with async_session() as session:
            yield session

    @staticmethod
    async def create_job(session: AsyncSession, job_data: Dict[str, Any]) -> Job:
        """Create a new job entry."""
        job = Job(**job_data)
        session.add(job)
        await session.commit()
        return job

    @staticmethod
    async def get_job(session: AsyncSession, job_id: int) -> Optional[Job]:
        """Get a job by ID."""
        result = await session.execute(
            select(Job).where(Job.id == job_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_candidate(session: AsyncSession, candidate_data: Dict[str, Any]) -> Candidate:
        """Create a new candidate entry."""
        candidate = Candidate(**candidate_data)
        session.add(candidate)
        await session.commit()
        return candidate

    @staticmethod
    async def get_candidate(session: AsyncSession, candidate_id: int) -> Optional[Candidate]:
        """Get a candidate by ID."""
        result = await session.execute(
            select(Candidate).where(Candidate.id == candidate_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_match(session: AsyncSession, match_data: Dict[str, Any]) -> Match:
        """Create a new match entry."""
        match = Match(**match_data)
        session.add(match)
        await session.commit()
        return match

    @staticmethod
    async def get_match(session: AsyncSession, match_id: int) -> Optional[Match]:
        """Get a match by ID."""
        result = await session.execute(
            select(Match).where(Match.id == match_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_match_status(session: AsyncSession, match_id: int, status: str) -> Optional[Match]:
        """Update the status of a match."""
        match = await DatabaseManager.get_match(session, match_id)
        if match:
            match.status = status
            await session.commit()
        return match

    @staticmethod
    async def create_interview(session: AsyncSession, interview_data: Dict[str, Any]) -> Interview:
        """Create a new interview entry."""
        interview = Interview(**interview_data)
        session.add(interview)
        await session.commit()
        return interview

    @staticmethod
    async def get_interview(session: AsyncSession, interview_id: int) -> Optional[Interview]:
        """Get an interview by ID."""
        result = await session.execute(
            select(Interview).where(Interview.id == interview_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_interview_status(session: AsyncSession, interview_id: int, status: str) -> Optional[Interview]:
        """Update the status of an interview."""
        interview = await DatabaseManager.get_interview(session, interview_id)
        if interview:
            interview.status = status
            await session.commit()
        return interview

    @staticmethod
    async def get_job_matches(session: AsyncSession, job_id: int) -> List[Match]:
        """Get all matches for a job."""
        result = await session.execute(
            select(Match).where(Match.job_id == job_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_candidate_matches(session: AsyncSession, candidate_id: int) -> List[Match]:
        """Get all matches for a candidate."""
        result = await session.execute(
            select(Match).where(Match.candidate_id == candidate_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_match_interview(session: AsyncSession, match_id: int) -> Optional[Interview]:
        """Get the interview for a match."""
        result = await session.execute(
            select(Interview).where(Interview.match_id == match_id)
        )
        return result.scalar_one_or_none() 