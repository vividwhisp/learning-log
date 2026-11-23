## Data Deletion Lifecycle

Current implementation:
- Source documents are stored as Markdown files.
- Chunks are generated into data/chunks.json.
- Qdrant stores chunk text and metadata as payload.
- index.py rebuilds the collection during reindexing.

Deletion procedure:
1. Remove the original document.
2. Regenerate chunks.json.
3. Rebuild the Qdrant collection.
4. Check logs, evaluations and backups for retained copies.

Limitation:
This is a local-project deletion workflow, not a
production-grade deletion or retention system.

# Day 55 — PII, Secrets & Data Privacy

## Groq Data Handling

- Groq acts as a data processor for GroqCloud customer data.
- Customer inputs and outputs are not used to train models for Groq's own purposes.
- Certain reliability and abuse-related events may result in temporary input/output logging.
- Relevant data may be retained for up to 30 days.
- Zero Data Retention (ZDR) is available through Groq Data Controls.
- Data is encrypted in transit using TLS 1.2+ and at rest using AES-256 GCM.

## Project Security Decisions

- Redact sensitive information before chunking and indexing.
- Avoid logging raw queries, retrieved content and generated answers.
- Avoid sending real customer secrets to external inference providers.
- Understand provider retention policies before processing user data.

## Limitations

- Regex-based PII detection is incomplete.
- Redaction is not a substitute for access control.
- Local document deletion must propagate to chunks and vector storage.
- Provider retention settings must be verified in the account.

## References

- https://console.groq.com/docs/your-data
- https://trust.groq.com/
- https://console.groq.com/settings/data-controls