local map = vim.keymap.set

local function opts(desc)
	return { noremap = true, silent = true, desc = desc }
end

-- Keep selection after indenting.
map("v", "<", "<gv", opts("Indent left"))
map("v", ">", ">gv", opts("Indent right"))

-- Clear search highlighting.
map("n", "<Esc>", "<cmd>nohlsearch<CR>", opts("Clear search highlight"))
map("n", "<leader>h", "<cmd>nohlsearch<CR>", opts("Clear search highlight"))

-- Better movement for wrapped lines.
map({ "n", "x" }, "j", "v:count == 0 ? 'gj' : 'j'", { expr = true, silent = true, desc = "Down" })
map({ "n", "x" }, "k", "v:count == 0 ? 'gk' : 'k'", { expr = true, silent = true, desc = "Up" })

-- Split navigation. This stays tmux-friendly and does not create panes automatically.
map("n", "<C-h>", "<C-w>h", opts("Move to left split"))
map("n", "<C-j>", "<C-w>j", opts("Move to lower split"))
map("n", "<C-k>", "<C-w>k", opts("Move to upper split"))
map("n", "<C-l>", "<C-w>l", opts("Move to right split"))

-- Buffers.
map("n", "<S-h>", "<cmd>bprevious<CR>", opts("Previous buffer"))
map("n", "<S-l>", "<cmd>bnext<CR>", opts("Next buffer"))
map("n", "<leader>bd", "<cmd>bdelete<CR>", opts("Delete buffer"))
map("n", "<leader>bo", "<cmd>%bdelete|edit #|bdelete #<CR>", opts("Delete other buffers"))

-- Diagnostics.
map("n", "[d", vim.diagnostic.goto_prev, opts("Previous diagnostic"))
map("n", "]d", vim.diagnostic.goto_next, opts("Next diagnostic"))
map("n", "<leader>e", vim.diagnostic.open_float, opts("Line diagnostics"))
map("n", "<leader>q", vim.diagnostic.setloclist, opts("Diagnostics to loclist"))

-- Quickfix/location lists.
map("n", "[q", "<cmd>cprevious<CR>", opts("Previous quickfix item"))
map("n", "]q", "<cmd>cnext<CR>", opts("Next quickfix item"))
map("n", "[l", "<cmd>lprevious<CR>", opts("Previous location item"))
map("n", "]l", "<cmd>lnext<CR>", opts("Next location item"))

-- Save.
map({ "n", "i", "x" }, "<C-s>", "<cmd>write<CR><Esc>", opts("Save file"))
