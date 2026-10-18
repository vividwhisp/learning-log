# PostgreSQL Fundamentals

## What PostgreSQL Is

PostgreSQL is an open-source relational database management system. It stores data in tables with defined schemas and supports SQL for querying and modifying records. PostgreSQL provides transactions, constraints, indexes, views, joins, and concurrency control. It is frequently used as the persistent data store behind web APIs and other application services.

A database server can host multiple databases, and each database can contain schemas and database objects such as tables, views, sequences, and functions. A role represents a database identity and can be granted permissions. In application deployments, development, testing, and production environments should use separate credentials and appropriately scoped permissions.

## Tables, Primary Keys, and Constraints

A table represents rows of related data. Each column has a data type, such as `integer`, `text`, `boolean`, `date`, `timestamp with time zone`, or `uuid`. A primary key uniquely identifies each row. A foreign key enforces a relationship to a key in another table or in the same table. `NOT NULL`, `UNIQUE`, and `CHECK` constraints encode data rules in the database rather than relying solely on application code.

Example schema:

```sql
CREATE TABLE projects (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tasks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES projects(id),
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

The `tasks.project_id` foreign key prevents a task from referencing a project that does not exist. The `completed` column defaults to `FALSE` when a new task is created without an explicit value. Defaults are not substitutes for constraints: `NOT NULL` still matters when a column must always contain a value.

## Basic SQL Queries

Use `SELECT` to read rows, `INSERT` to add rows, `UPDATE` to modify rows, and `DELETE` to remove rows. A `WHERE` clause restricts which rows an operation affects. An `ORDER BY` clause controls the returned order, and `LIMIT` caps the number of rows returned.

```sql
SELECT id, title, created_at
FROM tasks
WHERE project_id = 1 AND completed = FALSE
ORDER BY created_at DESC
LIMIT 20;

INSERT INTO tasks (project_id, title)
VALUES (1, 'Add API tests')
RETURNING id, title;

UPDATE tasks
SET completed = TRUE
WHERE id = 42
RETURNING id, completed;
```

An `UPDATE` or `DELETE` statement without an appropriate `WHERE` clause may affect every row in a table. Review destructive statements carefully and use a transaction when a sequence of changes must succeed or fail together.

## Joins and Aggregation

A join combines rows using a relationship between tables. An `INNER JOIN` returns rows with matching records on both sides. A `LEFT JOIN` preserves every row from the left side, even when there is no matching row on the right. Aggregate functions such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX` summarize groups of rows.

```sql
SELECT p.name, COUNT(t.id) AS task_count
FROM projects AS p
LEFT JOIN tasks AS t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY task_count DESC;
```

This query includes projects with no tasks because it uses a left join. `COUNT(t.id)` returns zero for a project with no matching task rows; counting all rows after an outer join can produce a different result.

## Transactions and ACID

A transaction groups database operations into one logical unit. PostgreSQL transactions support the ACID properties: atomicity, consistency, isolation, and durability. `BEGIN` starts an explicit transaction, `COMMIT` makes its changes permanent, and `ROLLBACK` discards uncommitted changes.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

The example illustrates a transfer that should update both accounts together. A production implementation must also validate that the source account exists and has sufficient funds, handle concurrent updates safely, and verify that each update affected the expected number of rows. If an error occurs before commit, the transaction can be rolled back.

PostgreSQL uses multiversion concurrency control (MVCC) so concurrent transactions can work with consistent versions of rows. Isolation levels control which concurrent changes a transaction can observe. Applications should be prepared to retry certain transactions when concurrency conflicts or serialization failures occur.

## Indexes and Query Performance

An index can speed up lookups and joins by helping PostgreSQL find matching rows without scanning the entire table. Indexes also consume storage and add work to inserts, updates, and deletes, so adding an index to every column is not a good strategy. B-tree is the default index type and supports many equality and range queries. Other index types, such as GIN, are useful for particular data types and operators.

```sql
CREATE INDEX idx_tasks_project_created
ON tasks (project_id, created_at DESC);
```

A multicolumn index is most effective when its column order matches useful query patterns. Use `EXPLAIN` to inspect a planned query and `EXPLAIN ANALYZE` to execute it and report actual timings and row counts. Analyze the query plan before adding indexes based only on intuition. Keep database statistics current so the planner can make informed choices.

## Connecting from a Python API

A service commonly reads database connection settings from environment variables rather than hard-coding credentials. A connection string may include the host, port, database name, username, and password; secrets should not be committed to source control. Connection pooling can reduce the overhead of repeatedly opening connections, especially in a request-driven API.

Always use parameterized queries when including user-supplied values. Do not build SQL by concatenating raw input into a query string, because doing so can create SQL injection vulnerabilities. Use a database driver's parameters or a reputable query builder or ORM. The parameter syntax differs between drivers, so follow the library's documentation.

## Backups, Migrations, and Reliability

Backups should be tested by restoring them, not merely by confirming that a backup command completed. A schema migration records a controlled change to database structure, such as creating a table or adding an index. Keep migrations in version control and apply them consistently across environments. For a production service, plan for connection limits, timeouts, slow queries, disk capacity, monitoring, and restore procedures.

A database container's writable filesystem is not a durable backup. Use a persistent volume for local development when data must survive container replacement, and maintain a separate backup strategy for valuable data. Protect database credentials, restrict network exposure, and grant an application role only the permissions its tasks require.
