# Personal agent instructions

These are shared personal defaults. Follow the current task and applicable
repository instructions; do not assume every project uses the same tools.

## Working style

- Inspect the existing code, documentation, and working-tree changes first.
- Make focused changes that follow the project's conventions. Preserve unrelated
  work, and do not reset, discard, stage, or commit changes unless requested.
- Prefer filesystem, CLI, and API operations over GUI automation when practical.
- Run relevant checks when possible. Report what changed, what was tested, and
  any failures or checks you could not run. Do not claim unperformed validation.
- Keep responses concise and identify changed files clearly. Use
  [unslop](skills/unslop/SKILL.md) without dropping facts or evidence.
- Search before reading large files, bound command output, and avoid rereading
  unchanged material already in context. Preserve evidence paths and unresolved
  questions when summarizing.

## Safety and configuration

- Never commit credentials, private keys, authentication state, or session logs.
  Do not print secrets while inspecting configuration.
- Ask before destructive operations, privileged system changes, or activating a
  NixOS/Home Manager configuration, unless the user already requested them.
- Treat third-party skills and extensions as executable guidance: review their
  instructions and bundled code before adopting them.
- Edit Home Manager-managed files in their source repository, not through their
  installed Nix-store symlinks. Do not force-replace conflicting local files.

## Skills

- Shared skills live in ~/.agents/skills/<name>/SKILL.md. Read a relevant skill
  before following its workflow, and resolve bundled paths from its directory.
- Before delegating or changing Git, tracker, or publication state, read the
  [shared workflow policy](skills/orchestration/references/workflow-policy.md).
  Use Orca for authorized delegation; ordinary work stays direct. Loading a
  skill does not expand the authority of the current request.
- Dotfiles-managed skills are read-only after activation. Update their source
  under ~/Projects/dotfiles/.agents/skills/, then validate and request activation.
- Leave unrelated installer-managed skills and their lock files alone. Avoid
  installing a second skill with the same name in another discovery location.
