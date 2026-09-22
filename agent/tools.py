"""Tools the agent can call. Read-only access to the Gold tables through DuckDB."""
import json
import re
from pathlib import Path

import duckdb

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "gold"
MAX_ROWS = 200

# Load every Gold parquet file into an in-memory DuckDB, then switch off file/network access.
_con = duckdb.connect(database=":memory:")
for _d in sorted(p for p in DATA_DIR.iterdir() if p.is_dir()):
    _con.execute(f'CREATE TABLE "{_d.name}" AS SELECT * FROM read_parquet(\'{_d.as_posix()}/*.parquet\')')
_con.execute("SET enable_external_access = false")

_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|create|alter|attach|detach|copy|pragma|install|load|export|import|call|set|truncate|replace|merge)\b",
    re.IGNORECASE,
)


def list_tables() -> dict:
    """Lists the tables the analyst can query, with their columns.

    Returns:
        dict with a 'tables' entry mapping table name -> list of column names.
    """
    tables = {}
    for (name,) in _con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall():
        cols = _con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position", [name]
        ).fetchall()
        tables[name] = [c[0] for c in cols]
    return {"status": "success", "tables": tables}


def run_sql(query: str) -> dict:
    """Runs ONE read-only SQL query (DuckDB dialect) against the Gold tables.

    Args:
        query: a single SELECT statement (WITH ... SELECT is allowed).

    Returns:
        dict with 'status' and either 'rows' (at most 200) or an 'error' message.
    """
    q = query.strip().rstrip(";").strip()
    if ";" in q:
        return {"status": "error", "error": "Only one statement is allowed."}
    if not re.match(r"^(select|with)\b", q, re.IGNORECASE):
        return {"status": "error", "error": "Only SELECT queries are allowed."}
    if _FORBIDDEN.search(q):
        return {"status": "error", "error": "This query contains a forbidden keyword. Only read-only SELECT queries are allowed."}
    try:
        df = _con.execute(f"SELECT * FROM ({q}) AS t LIMIT {MAX_ROWS}").fetchdf()
    except Exception as exc:  # let the model see the error and fix its SQL
        return {"status": "error", "error": str(exc)}
    return {"status": "success", "row_count": len(df), "rows": json.loads(df.to_json(orient="records", date_format="iso"))}