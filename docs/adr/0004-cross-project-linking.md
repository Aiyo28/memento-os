# Link knowledge across projects with MOC hubs, extracted patterns and a controlled tag taxonomy

Seven projects each produced research, decisions and patterns that the others could not see; the same debugging fix was re-discovered after two weeks because the note existed but was not findable. Three approaches failed at discovery: one flat shared folder (unnavigable at 60+ files), free-form tags (100+ overlapping tags for 30 documents) and on-demand full-text search (misses semantic matches, and the agent has no signal that anything exists). We use three mechanisms:

- **MOC hub files** — four hubs in `Knowledge/` hold links and one-line summaries across all projects, no content. One read shows related work without loading it.
- **Pattern extraction** — a reusable insight is extracted to `Knowledge/patterns/` in a project-neutral schema (Context / Pattern / Why / Verified In), so a pattern is found by what it is, not by where it was first discovered.
- **Canonical tag taxonomy** — one controlled list in `Knowledge/meta/tag-taxonomy.md`, referenced from the global `CLAUDE.md`. Tags are `domain/subtopic`, two levels at most; project identity goes in a `project:` frontmatter field, never as a tag; check the taxonomy before adding a tag and propose additions separately.

Together they form a graph the agent can navigate without loading it: MOCs are hubs, project `_context.md` files are spokes, pattern files are shared nodes, tags are edges. Observed: a stored CORS header-order fix was retrieved in a third project in under 5 minutes (45 minutes without it); the pattern library reached 6 entries in 3 weeks, each reused in a project other than its origin; tags stabilised at 23 across 40+ documents.

Open: whether MOCs need their own hierarchy at 15+ projects, whether the agent should propose pattern extraction mid-session, whether back-link counts can flag under-connected documents, and what review is needed before agents write to MOCs autonomously.
