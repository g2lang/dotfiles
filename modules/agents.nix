{ config, lib, ... }:

let
  instructions = ../.agents/AGENTS.md;
  # Add each new agent's global instruction path here. These aliases point to
  # the canonical installed file rather than maintaining per-agent copies.
  instructionAliases = [
    ".pi/agent/AGENTS.md"
    ".codex/AGENTS.md"
  ];
  aliasFiles = lib.genAttrs instructionAliases (_: {
    source = config.lib.file.mkOutOfStoreSymlink "${config.home.homeDirectory}/.agents/AGENTS.md";
  });
  skillsDirectory = ../.agents/skills;
  # Each directory is one explicitly vendored skill. Never manage the entire
  # ~/.agents directory: installers and unmanaged skills must remain writable.
  skills = lib.filterAttrs (_: type: type == "directory") (builtins.readDir skillsDirectory);
  skillFiles = lib.mapAttrs' (
    name: _:
    lib.nameValuePair ".agents/skills/${name}" {
      source = skillsDirectory + "/${name}";
    }
  ) skills;
in
{
  assertions = lib.mapAttrsToList (name: _: {
    assertion =
      builtins.match "[a-z0-9]+(-[a-z0-9]+)*" name != null
      && builtins.stringLength name <= 64
      && builtins.pathExists (skillsDirectory + "/${name}/SKILL.md");
    message = "Managed agent skill '${name}' needs a portable lowercase-hyphenated name and SKILL.md.";
  }) skills;

  # Pi and Codex both discover ~/.agents/skills natively; no duplicate skill
  # installation or whole-directory aliases are needed for these clients.
  home.file =
    skillFiles
    // aliasFiles
    // {
      ".agents/AGENTS.md".source = instructions;
    };
}
