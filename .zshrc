# Interactive configuration only; safe to source from a script without side effects.
[[ -o interactive ]] || return 0

export EDITOR=nvim
export VISUAL=nvim
export PAGER=less
export LESS='-R -F -X'

export PATH=~/.cargo/bin:$PATH

# Keep the existing history location, shared between shells. A leading space
# opts a command out of history, but is not a substitute for secret handling.
HISTFILE="$HOME/.zsh_history"
HISTSIZE=100000
SAVEHIST=100000
setopt EXTENDED_HISTORY SHARE_HISTORY HIST_FCNTL_LOCK
setopt HIST_IGNORE_SPACE HIST_IGNORE_ALL_DUPS HIST_SAVE_NO_DUPS
setopt HIST_FIND_NO_DUPS HIST_REDUCE_BLANKS HIST_VERIFY
setopt AUTO_CD AUTO_PUSHD PUSHD_IGNORE_DUPS INTERACTIVE_COMMENTS

# Completion stays local to the user; retain compinit's permission checks.
autoload -Uz compinit
if ((! $+functions[compdef])); then
  typeset _cxf_zsh_cache="${XDG_CACHE_HOME:-$HOME/.cache}/zsh"
  if mkdir -p -- "$_cxf_zsh_cache"; then
    compinit -d "$_cxf_zsh_cache/zcompdump-$ZSH_VERSION"
  else
    compinit -D
  fi
  unset _cxf_zsh_cache
fi
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%F{blue}-- %d --%f'
zstyle ':completion:*' verbose yes
zstyle ':completion:*:processes' command 'ps -u $USER -o pid,stat,comm'

# Vi editing, with familiar insert-mode navigation and a usable Escape timeout
# over SSH. Ctrl-R is upgraded by fzf below when available.
bindkey -v
KEYTIMEOUT=10
bindkey -M viins '^A' beginning-of-line
bindkey -M viins '^E' end-of-line
bindkey -M viins '^P' history-beginning-search-backward
bindkey -M viins '^N' history-beginning-search-forward
bindkey -M viins '^R' history-incremental-search-backward
bindkey -M viins '^?' backward-delete-char
bindkey -M viins '^H' backward-delete-char
bindkey -M viins '^[[A' history-beginning-search-backward
bindkey -M viins '^[[B' history-beginning-search-forward
bindkey -M viins '^[[H' beginning-of-line
bindkey -M viins '^[[F' end-of-line
bindkey -M viins '^[[3~' delete-char
zmodload zsh/terminfo
[[ -n ${terminfo[kcuu1]} ]] && bindkey -M viins "${terminfo[kcuu1]}" history-beginning-search-backward
[[ -n ${terminfo[kcud1]} ]] && bindkey -M viins "${terminfo[kcud1]}" history-beginning-search-forward
[[ -n ${terminfo[khome]} ]] && bindkey -M viins "${terminfo[khome]}" beginning-of-line
[[ -n ${terminfo[kend]} ]] && bindkey -M viins "${terminfo[kend]}" end-of-line
[[ -n ${terminfo[kdch1]} ]] && bindkey -M viins "${terminfo[kdch1]}" delete-char

# Ctrl-X Ctrl-E edits the current command in Neovim rather than executing it.
autoload -Uz edit-command-line
zle -N edit-command-line
bindkey -M viins '^X^E' edit-command-line
bindkey -M vicmd 'v' edit-command-line

if (($+commands[eza])); then
  alias ls='eza --group-directories-first'
  alias ll='eza -lah --group-directories-first'
  alias la='eza -a --group-directories-first'
fi
(($+commands[rg])) && alias grep='rg'
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate'
alias ..='cd ..'
alias ...='cd ../..'
alias v='nvim'

mkcd() {
  if (($# != 1)); then
    print -u2 'usage: mkcd <directory>'
    return 2
  fi
  mkdir -p -- "$1" && builtin cd -- "$1"
}

croot() {
  local root
  root=$(git rev-parse --show-toplevel 2>/dev/null) || {
    print -u2 'croot: not inside a Git worktree'
    return 1
  }
  builtin cd -- "$root"
}

# Native integrations rather than a shell framework or runtime plugin manager.
(($+commands[zoxide])) && eval "$(zoxide init zsh)"
if (($+commands[fzf])); then
  export FZF_DEFAULT_OPTS='--height=45% --layout=reverse --border=rounded --color=bg+:#313244,fg:#cdd6f4,fg+:#cdd6f4,hl:#f38ba8,hl+:#f38ba8,pointer:#cba6f7,prompt:#89b4fa,info:#a6adc8'
  if (($+commands[fd])); then
    export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'
    export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    export FZF_ALT_C_COMMAND='fd --type d --hidden --exclude .git'
  fi
  if (($+commands[bat])); then
    export FZF_CTRL_T_OPTS='--preview "bat --color=always --style=numbers --line-range=:200 -- {}" --preview-window=right:55%:wrap'
  fi
  if (($+commands[eza])); then
    export FZF_ALT_C_OPTS='--preview "eza --tree --level=2 --color=always -- {}"'
  fi
  source <(fzf --zsh)
fi

# These files are supplied by pinned Nix packages, never fetched at shell startup.
typeset _cxf_zsh_plugins="${XDG_CONFIG_HOME:-$HOME/.config}/zsh/plugins"
ZSH_AUTOSUGGEST_STRATEGY=(history)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'
ZSH_AUTOSUGGEST_USE_ASYNC=1
if [[ -r "$_cxf_zsh_plugins/zsh-autosuggestions.zsh" ]]; then
  source "$_cxf_zsh_plugins/zsh-autosuggestions.zsh"
  bindkey -M viins '^@' autosuggest-accept
fi

# A dependency-free fallback also works before Home Manager is activated.
PROMPT='%F{blue}%n@%m%f:%F{cyan}%~%f %# '
(($+commands[starship])) && eval "$(starship init zsh)"
(($+commands[direnv])) && eval "$(direnv hook zsh)"

# Personal additions stay outside the managed file. Highlighting loads last so
# it can observe widgets installed by integrations and local customizations.
[[ -r "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"
if [[ -r "$_cxf_zsh_plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "$_cxf_zsh_plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi
unset _cxf_zsh_plugins
