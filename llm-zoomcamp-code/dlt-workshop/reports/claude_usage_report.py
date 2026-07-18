import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    from pathlib import Path

    db_path = Path("/workspaces/llm-zoomcamp/llm-zoomcamp-code/dlt-workshop/.dlt/data/dev/claude_logs_pipeline.duckdb")
    con = duckdb.connect(str(db_path))
    return (con,)


@app.cell
def _(con):
    summary_query = """
    SELECT
        source_file,
        line_number,
        parsed_json,
        raw_json
    FROM claude_logs.claude_logs
    ORDER BY source_file, line_number
    """
    rows = con.execute(summary_query).fetchall()
    rows = [
        {
            "source_file": row[0],
            "line_number": row[1],
            "parsed_json": row[2],
            "raw_json": row[3],
        }
        for row in rows
    ]
    rows[:5]
    return (rows,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Claude Code usage report
    """)
    return


@app.cell
def _(mo, rows):
    mo.md("## Raw data preview")
    mo.ui.table(rows[:20])
    return


@app.cell
def _(con, mo):
    stats_query = """
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT source_file) AS distinct_files,
        MAX(line_number) AS max_lines_per_file
    FROM claude_logs.claude_logs
    """
    stats = con.execute(stats_query).fetchall()
    stats = [
        {"total_rows": row[0], "distinct_files": row[1], "max_lines_per_file": row[2]}
        for row in stats
    ]
    mo.ui.table(stats)
    return


@app.cell
def _(con, mo):
    session_counts_query = """
    SELECT
        source_file AS session_file,
        COUNT(*) AS rows
    FROM claude_logs.claude_logs
    GROUP BY source_file
    ORDER BY rows DESC
    LIMIT 15
    """
    session_counts = con.execute(session_counts_query).fetchall()
    session_counts = [
        {"session_file": row[0], "rows": row[1]}
        for row in session_counts
    ]
    mo.ui.table(session_counts)
    return


if __name__ == "__main__":
    app.run()
