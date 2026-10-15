# Promote decisions out of conversation and session logs into durable storage

Status: open. No mechanism chosen beyond the artifact format.

Decisions made in a conversation live only in the context window, in append-only session logs nobody rereads, or in the developer's memory. An audit of 12 sessions on one project found 14+ decisions that never reached a decisions file or typed memory entry, so they were later re-made, sometimes differently. The direction is to graduate decisions into `[D]` artifacts with an invalidation trigger (see `docs/GLOSSARY.md`, "Decision graduation").

Open: what counts as a decision worth graduating, whether graduation is real-time or a batch review, and whether a reversal supersedes the old entry or amends it.
