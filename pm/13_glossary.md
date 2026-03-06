# Glossary

This glossary is normative for the project. Future sessions should not rely on casual or ambiguous meanings when these terms appear in planning or implementation.

## Evidence Terms

### Raw Evidence

Unmodified bytes fetched from lawful public sources and stored immutably in the evidence object store.

### Manifest

The structured ingest record describing discovery or download of a source object, including source URL, fetch time, headers, MIME type, size, and hash.

### Document

The canonical top-level evidence object representing one source file in structured form.

### Page

The canonical evidence object representing one document page, including image reference, geometry, and extraction confidence metadata.

### Span

The atomic evidence-backed textual unit. This is the primary truth object for citation and downstream inspection.

### Claim

A structured assertion derived from spans and carrying subject, predicate, object or literal, provenance, confidence, and review state.

### Provenance Tuple

The required lineage bundle tying a derived artifact back to its source and processing state:

- source URL
- fetch timestamp
- SHA-256
- lakeFS commit
- Iceberg snapshot identifier
- extractor version
- model version when applicable

### Native Text

Text directly extracted from the source file without OCR.

### OCR Text

Text reconstructed from page imagery by OCR engines when native text is missing or unreliable.

### Extraction Engine Identity

The named engine or library responsible for a text or layout output, such as `pypdf`, `pymupdf`, `unstructured`, `tesseract`, `doctr`, or `trocr`.

## Policy Terms

### Sensitivity

The safe-handling classification applied before indexing, summarization, embedding, QA prompting, or broad analyst exposure.

### Restricted Context

Evidence or neighboring context that exists in the system but is not broadly visible due to policy or role restrictions.

### Unsafe For LLM

A sensitivity state indicating the content must not be sent to a synthesis or judging model under normal operations.

### Review State

The lifecycle state indicating whether an artifact is pending review, accepted, rejected, deferred, or otherwise governed by adjudication.

### Policy Context

The explicit explanation of what role, restrictions, masking rules, and access decisions governed a result or response.

### Export Policy

The rule set governing what may be exported, by whom, at what granularity, and under what review controls.

## Analytical Terms

### Derived Artifact

Any artifact produced from evidence processing or analytical synthesis rather than stored as raw source evidence.

### Canonical Fact

A structured fact promoted to the canonical analytical layer after required review or validation, distinct from hypotheses and unresolved candidates.

### Alias Candidate

A possible alternate name or identity marker tied to source evidence but not yet merged into canonical identity.

### Event

An evidence-backed structured occurrence with participants, time interval, location, evidence support, and confidence.

### Topic

A derived semantic grouping of related texts or artifacts. Topics are never primary evidence.

### Sense Cluster

A derived grouping of similar contextual uses of a term for analyst review. It is a hypothesis, not a decoded truth.

### Evidence Pack

The assembled set of policy-filtered, ranked, citation-ready sources used to support a QA response or analyst synthesis.

### Support State

The explicit QA state indicating whether an answer is fully supported, partially supported, or insufficiently supported.

### Abstention

The behavior in which QA declines to generate a narrative answer and instead returns evidence or an explanation of insufficient support.

## Delivery Terms

### Phase

A major program slice with explicit entry criteria, exit criteria, and handoff obligations.

### Task

A bounded work item that produces a durable output and can be owned by one senior contributor or subagent.

### Subtask

A concrete execution step within a task.

### Work Package

The scoped assignment wrapper for one contributor or subagent.

### Blocking Dependency

A predecessor that must complete before dependent work may start.

### Soft Dependency

A predecessor that improves quality, integration, or speed but does not strictly block start.

### Parallelizable Work

Work that may proceed concurrently without violating sequencing or creating uncontrolled ownership conflict.

### Critical Path

The narrowest dependency chain whose delay delays the target milestone.

### Promotion

The act of making a derived artifact available to broader downstream systems or user-facing surfaces.

### Rematerialization

The controlled regeneration of derived artifacts after upstream inputs, policy rules, or review decisions change.

### Gold Set

A curated, reviewed evaluation dataset used to calibrate thresholds and test model-assisted workflows.
