# Shared agent configuration

Home Manager manages shared personal instructions and selected skills from this
repository. `modules/agents.nix`, imported by `home.nix`, owns the installation.
It does not manage agent logins, runtime state, or tool settings.

## One canonical location

After activation, the logical layout is:

```text
~/.agents/
  AGENTS.md                     -> Nix-store-backed instructions
  skills/
    codebase-design/             -> Nix-store-backed skill directory
    <unmanaged skills>/         # Existing installer-managed skills stay here
~/.pi/agent/AGENTS.md            -> ~/.agents/AGENTS.md
~/.codex/AGENTS.md               -> ~/.agents/AGENTS.md
```

Home Manager may insert an intermediate Nix-store symlink for aliases; resolving
one still reaches the canonical `~/.agents/AGENTS.md`. There are no per-agent
copies to synchronize and no dependency on a live checkout after activation.

Edit `.agents/AGENTS.md` here to change personal defaults. Repository-specific
instructions still belong in each project's own `AGENTS.md`.

Pi and Codex both discover `~/.agents/skills/` natively, including symlinked skill
directories. We do not also install these skills under their tool-specific skill
paths, avoiding duplicate discovery. Pi supports `/skill:codebase-design`;
Codex supports `$codebase-design` or its `/skills` selector. Reload Pi with
`/reload` after activation; restart an agent if it has cached instructions or
skill discovery.

## Workflow composition

The installed shared policy lives at
`~/.agents/skills/orchestration/references/workflow-policy.md`. It distinguishes
ordinary direct work, an Orca ownership handoff, and supervised Orca tasks.
The Orca skill stubs load command and lifecycle instructions from the installed
CLI. Do not copy those command catalogs into every workflow.

Engineering principles and `benchmark-checklist` are automatically selectable.
Design competitions, independent review, multi-ticket implementation, corrective
cleanup, and planning/publication procedures remain explicit commands. Matching
`agents/openai.yaml` policies keep explicit commands consistent for Codex.
Selection is not guaranteed, and loading a skill never grants extra permissions.

`handoff-note` replaces the former `handoff` command. It writes a private
continuation note only. Use `orca-cli` to transfer ownership and `orchestration`
to supervise work. Existing clients need a reload after activation to discover
the renamed command.

`implement-spec` separates implementation tasks from integration-and-verification
tasks. Dependent builds wait for verified integration, not merely for a worker's
completion. One owner writes the integration branch. Review is read-only unless
fixes are separately assigned. Commit, publication, merge, and worktree-deletion
permissions are established at the relevant phase.

Project tracker configuration remains project-local. The shared reference at
`~/.agents/skills/to-tickets/references/project-workflow.md` explains how planning
skills use it without requiring another setup workflow. Generated verification skills
belong in the target project's `.agents/skills/`, not the global collection.

`just test-agents` checks metadata and Home Manager wiring, local Markdown
references, unsupported tool assumptions, and invocation-policy agreement.
The checks do not prove workflow behavior. After execution-policy changes, run a
small explicitly authorized Orca review against fixed inputs, process questions
and completion through the installed guide, inspect the report, and release the
settled worker. Record blocked or unverified steps rather than treating static
tests as a runtime proof. Keep run receipts and reports outside this checkout.

## Add, update, or remove a managed skill

Each immediate directory in `.agents/skills/` is installed as **one directory
symlink**, not as a writable copy or a symlink for the entire skills collection.
New skill directories are discovered automatically by the Nix module; there is
no second manifest to edit.

1. Create `.agents/skills/my-skill/SKILL.md` with portable frontmatter:

   ```markdown
   ---
   name: my-skill
   description: Describe the specific task this skill handles and when to use it.
   ---

   # My skill

   Instructions go here. Resolve bundled paths relative to this directory.
   ```

2. Include any required `scripts/`, `references/`, or `assets/` inside that skill
   directory. Link dependencies using relative Markdown paths so tests can check
   them. Resolve links from the file that contains them, not the working
   directory. Use lowercase names with single hyphens, at most 64 characters,
   and match the directory name to the frontmatter name. Keep descriptions on
   one line (at most 1024 characters).
3. Run `just test-agents` and `just check`. Review new files as well as diffs.
4. When ready, activate explicitly with `just switch`. Until then, the currently
   installed instructions and skills are unchanged.

To update a managed skill, edit its sources here and repeat validation and
activation. To remove one, delete its source directory and activate; Home Manager
removes the managed link without removing unrelated skills.

For third-party skills, vendor only the reviewed skill directory and needed
support files. Preserve its license and record the upstream URL and commit in a
file such as `UPSTREAM.md` inside it. Updates are explicit reviewed changes, not
an unpinned download during activation. Inspect scripts, instructions, and
symlinks before importing; do not bundle private data or references into your
home directory. The Nix store is not a place for secrets.

Existing skills installed with another tool remain unmanaged until deliberately
migrated. Do not run an installer against a Nix-managed skill name: it cannot
update read-only store contents. Leave `~/.agents/.skill-lock.json` and unrelated
skill directories under their existing installer's control.

## First activation and conflicts

Run `just status`, `just check`, and `just test-agents` before activation.
Optionally use `just build` or `just diff` to review a build without switching.
No test or validation recipe activates the configuration.

Home Manager refuses conflicting files; no forced replacement is configured.
If a destination already exists (for example `~/.codex/AGENTS.md` or a skill of
the same name), inspect it, merge any desired contents into the versioned source,
and move **only that conflicting file or skill directory** to an unused backup
path outside the checkout before activation. Never move an entire live agent
directory or overwrite it just to install these files.

## Add another agent

Add its documented global instruction path to `instructionAliases` in
`modules/agents.nix`. The module creates a symlink to `~/.agents/AGENTS.md` using
Home Manager's `mkOutOfStoreSymlink`; the canonical file remains Nix-managed.
Respect any environment-variable overrides for that tool's configuration root.

If it discovers `~/.agents/skills/`, no other configuration is necessary. If it
requires a tool-specific skills directory, add **per-skill aliases** pointing to
`~/.agents/skills/<name>` using the same helper. Do not alias its whole skills
directory over existing built-in or installer-managed skills. Confirm the tool
follows directory symlinks and does not double-load skills.

## Boundaries

Only `.agents/AGENTS.md`, its explicit agent aliases, and the selected skill
directories are managed. Leave these outside Git and Home Manager management:

- Authentication files, API keys, OAuth tokens, and private MCP credentials.
- Sessions, history, logs, databases, caches, and trust records.
- Pi's npm package installations and package-manager metadata.
- Agent settings that need to remain writable through interactive commands.

Do not copy `~/.pi/agent`, `~/.codex`, or `~/.agents` wholesale into the checkout.
Ignored private files may still enter the Nix store through a `path:` flake.
