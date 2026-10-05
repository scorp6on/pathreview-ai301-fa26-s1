"""Tests for api/routes/health.py"""

from contextlib import suppress
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from sqlalchemy.sql.elements import TextClause

from api.routes.health import health_check


@pytest.mark.unit
class TestHealthCheck:
    """Test suite for the health check route."""

    @pytest.mark.asyncio
    async def test_postgres_probe_executes_textual_sql(self):
        """The postgres probe passes a text() clause, not a bare string (#61)."""
        db = AsyncMock()

        # The redis check (#62) can still fail, which makes the handler raise 503.
        with suppress(HTTPException):
            await health_check(db=db)

        db.execute.assert_awaited_once()
        statement = db.execute.await_args.args[0]
        assert isinstance(statement, TextClause)
        assert statement.text == "SELECT 1"
