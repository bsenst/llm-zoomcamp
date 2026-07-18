import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import dlt

    pipeline = dlt.attach(
        "agent_logs_pipeline",
        destination="playground",
        dataset_name="agent_logs",
    )
    con = pipeline.dataset()._dbapi_connection()
    return (con,)


@app.cell
def _(con):
    query = """
    SELECT
        index,
        session_id,
        type,
        timestamp,
        cwd,
        git_branch,
        version,
        message_role,
        message_text,
        model,
        input_tokens,
        output_tokens
    FROM agent_logs.agent_logs
    ORDER BY index
    """
    rows = con.execute(query).fetchall()
    rows = [
        {
            "index": row[0],
            "session_id": row[1],
            "type": row[2],
            "timestamp": row[3],
            "cwd": row[4],
            "git_branch": row[5],
            "version": row[6],
            "message_role": row[7],
            "message_text": row[8],
            "model": row[9],
            "input_tokens": row[10],
            "output_tokens": row[11],
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
    # Agent logs report
    """)
    return


@app.cell
def _(mo, rows):
    mo.md("## Sample rows")
    mo.ui.table(rows[:20])
    return


@app.cell
def _(con, mo):
    stats_query = """
    SELECT
        COUNT(*) AS total_logs,
        COUNT(DISTINCT session_id) AS distinct_sessions,
        COUNT(DISTINCT cwd) AS distinct_projects,
        COUNT(DISTINCT model) AS distinct_models,
        SUM(COALESCE(input_tokens, 0)) AS total_input_tokens,
        SUM(COALESCE(output_tokens, 0)) AS total_output_tokens
    FROM agent_logs.agent_logs
    """
    stats = con.execute(stats_query).fetchall()
    stats = [
        {
            "total_logs": row[0],
            "distinct_sessions": row[1],
            "distinct_projects": row[2],
            "distinct_models": row[3],
            "total_input_tokens": row[4],
            "total_output_tokens": row[5],
        }
        for row in stats
    ]
    mo.ui.table(stats)
    return


@app.cell
def _(con, mo):
    top_sessions_query = """
    SELECT
        session_id,
        COUNT(*) AS log_count,
        MAX(timestamp) AS last_seen,
        MAX(COALESCE(input_tokens, 0)) AS max_input_tokens,
        MAX(COALESCE(output_tokens, 0)) AS max_output_tokens
    FROM agent_logs.agent_logs
    GROUP BY session_id
    ORDER BY log_count DESC
    LIMIT 15
    """
    top_sessions = con.execute(top_sessions_query).fetchall()
    top_sessions = [
        {
            "session_id": row[0],
            "log_count": row[1],
            "last_seen": row[2],
            "max_input_tokens": row[3],
            "max_output_tokens": row[4],
        }
        for row in top_sessions
    ]
    mo.ui.table(top_sessions)
    return


@app.cell
def _(con, mo):
    by_type_query = """
    SELECT
        type,
        COUNT(*) AS count
    FROM agent_logs.agent_logs
    GROUP BY type
    ORDER BY count DESC
    """
    by_type = con.execute(by_type_query).fetchall()
    by_type = [
        {"type": row[0], "count": row[1]}
        for row in by_type
    ]
    mo.ui.table(by_type)
    return


if __name__ == "__main__":
    app.run()
