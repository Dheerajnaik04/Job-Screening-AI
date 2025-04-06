from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from contextlib import contextmanager
import os

# Database URL
DATABASE_URL = "sqlite+aiosqlite:///./job_screening.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@contextmanager
def get_session():
    """Get a database session."""
    session = async_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

async def init_db():
    """Initialize the database."""
    from .models import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Close the database connection."""
    await engine.dispose()

# Database operations
class DatabaseManager:
    @staticmethod
    async def create_job(session, job_data):
        """Create a new job entry."""
        from .models import Job
        job = Job(**job_data)
        session.add(job)
        await session.commit()
        return job

    @staticmethod
    async def create_candidate(session, candidate_data):
        """Create a new candidate entry."""
        from .models import Candidate
        candidate = Candidate(**candidate_data)
        session.add(candidate)
        await session.commit()
        return candidate

    @staticmethod
    async def create_match(session, match_data):
        """Create a new match entry."""
        from .models import Match
        match = Match(**match_data)
        session.add(match)
        await session.commit()
        return match

    @staticmethod
    async def create_interview(session, interview_data):
        """Create a new interview entry."""
        from .models import Interview
        interview = Interview(**interview_data)
        session.add(interview)
        await session.commit()
        return interview

    @staticmethod
    async def get_job_matches(session, job_id):
        """Get all matches for a job."""
        from .models import Match
        query = await session.execute(
            select(Match)
            .where(Match.job_id == job_id)
            .order_by(Match.match_score.desc())
        )
        return query.scalars().all()

    @staticmethod
    async def get_candidate_matches(session, candidate_id):
        """Get all matches for a candidate."""
        from .models import Match
        query = await session.execute(
            select(Match)
            .where(Match.candidate_id == candidate_id)
            .order_by(Match.match_score.desc())
        )
        return query.scalars().all()

    @staticmethod
    async def update_match_status(session, match_id, status):
        """Update the status of a match."""
        from .models import Match
        match = await session.get(Match, match_id)
        if match:
            match.status = status
            await session.commit()
        return match 