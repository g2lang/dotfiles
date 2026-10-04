local augroup = vim.api.nvim_create_augroup
local autocmd = vim.api.nvim_create_autocmd

local general = augroup("UserGeneral", { clear = true })

-- Highlight on yank.
autocmd("TextYankPost", {
	group = general,
	callback = function()
		vim.highlight.on_yank({ higroup = "IncSearch", timeout = 180 })
	end,
})

-- Restore cursor position.
autocmd("BufReadPost", {
	group = general,
	callback = function(event)
		local mark = vim.api.nvim_buf_get_mark(event.buf, '"')
		local line_count = vim.api.nvim_buf_line_count(event.buf)
		if mark[1] > 0 and mark[1] <= line_count then
			pcall(vim.api.nvim_win_set_cursor, 0, mark)
		end
	end,
})

-- Language-specific editing defaults.
autocmd("FileType", {
	group = general,
	pattern = { "rust", "python", "markdown", "nix", "toml", "yaml", "json", "lua" },
	callback = function()
		vim.opt_local.formatoptions:remove({ "o" })
	end,
})

autocmd("FileType", {
	group = general,
	pattern = { "markdown", "gitcommit" },
	callback = function()
		vim.opt_local.wrap = true
		vim.opt_local.linebreak = true
		vim.opt_local.spell = true
		vim.opt_local.conceallevel = 2
	end,
})

autocmd("FileType", {
	group = general,
	pattern = "python",
	callback = function()
		vim.opt_local.tabstop = 4
		vim.opt_local.shiftwidth = 4
		vim.opt_local.softtabstop = 4
	end,
})
