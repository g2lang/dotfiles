local opt = vim.opt

-- UI
opt.number = true
opt.relativenumber = true
opt.cursorline = true
opt.termguicolors = true
opt.signcolumn = "yes"
opt.wrap = false
opt.linebreak = true
opt.list = true
opt.listchars = { tab = "» ", trail = "·", nbsp = "␣", extends = "›", precedes = "‹" }
opt.fillchars = { eob = " ", fold = " ", foldopen = "", foldclose = "" }
opt.showmode = false
opt.cmdheight = 1
opt.laststatus = 3
opt.pumheight = 12
opt.scrolloff = 8
opt.sidescrolloff = 8
opt.splitright = true
opt.splitbelow = true

-- Editing
opt.tabstop = 2
opt.shiftwidth = 2
opt.softtabstop = 2
opt.expandtab = true
opt.smartindent = true
opt.breakindent = true
opt.confirm = true
opt.virtualedit = "block"
opt.inccommand = "split"
opt.completeopt = { "menu", "menuone", "noselect" }

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true
opt.hlsearch = true

-- Files
opt.undofile = true
opt.swapfile = false
opt.backup = false
opt.writebackup = false
opt.updatetime = 250
opt.timeoutlen = 400

-- Folding via Treesitter/LSP; keep folds open by default.
opt.foldlevel = 99
opt.foldlevelstart = 99
opt.foldenable = true

-- Use the OS clipboard when available. wl-clipboard is installed by Home Manager.
opt.clipboard = "unnamedplus"

-- Spell additions need to be writable. Home Manager links ~/.config/nvim to a
-- Nix-store generation, so keep the personal dictionary in Neovim state.
vim.fn.mkdir(vim.fn.stdpath("state") .. "/spell", "p")
opt.spelllang = { "en_us" }
opt.spellfile = vim.fn.stdpath("state") .. "/spell/en.utf-8.add"

-- Neovim providers. Python comes from Home Manager's python-with-packages.
vim.g.python3_host_prog = "python3"

-- Disable providers that are not needed for this setup.
vim.g.loaded_ruby_provider = 0
vim.g.loaded_perl_provider = 0
