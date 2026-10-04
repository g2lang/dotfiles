local function current_markdown_file()
	local file = vim.api.nvim_buf_get_name(0)
	if file == "" then
		vim.notify("Save this Markdown buffer before previewing it with glow", vim.log.levels.WARN)
		return nil
	end

	if vim.bo.modified then
		vim.cmd.write()
	end

	return file
end

local function glow_preview()
	local file = current_markdown_file()
	if not file then
		return
	end

	vim.cmd("!glow --pager " .. vim.fn.shellescape(file))
end

local function glow_tmux_split()
	local file = current_markdown_file()
	if not file then
		return
	end

	if vim.env.TMUX == nil then
		glow_preview()
		return
	end

	vim.fn.jobstart({ "tmux", "split-window", "-h", "glow", "--pager", file }, { detach = true })
end

vim.api.nvim_create_user_command("MarkdownPreview", glow_preview, {
	desc = "Preview the current Markdown file with glow",
})
vim.api.nvim_create_user_command("MarkdownPreviewTmux", glow_tmux_split, {
	desc = "Preview the current Markdown file with glow in a tmux split",
})
vim.api.nvim_create_user_command("GlowPreview", glow_preview, {
	desc = "Preview the current Markdown file with glow",
})
vim.api.nvim_create_user_command("GlowPreviewTmux", glow_tmux_split, {
	desc = "Preview the current Markdown file with glow in a tmux split",
})

-- User-defined Ex commands must start with an uppercase letter, so provide
-- command-line abbreviations for the natural lowercase forms too.
vim.cmd([[cnoreabbrev <expr> mp getcmdtype() == ':' && getcmdline() ==# 'mp' ? 'MarkdownPreview' : 'mp']])
vim.cmd([[cnoreabbrev <expr> mP getcmdtype() == ':' && getcmdline() ==# 'mP' ? 'MarkdownPreviewTmux' : 'mP']])

return {
	{
		"MeanderingProgrammer/render-markdown.nvim",
		ft = { "markdown", "Avante", "codecompanion" },
		dependencies = { "nvim-treesitter/nvim-treesitter", "nvim-tree/nvim-web-devicons" },
		opts = {
			enabled = true,
			render_modes = { "n", "c", "t" },
			heading = {
				sign = false,
				icons = { "󰲡 ", "󰲣 ", "󰲥 ", "󰲧 ", "󰲩 ", "󰲫 " },
			},
			code = {
				sign = false,
				width = "block",
				right_pad = 1,
			},
			bullet = { icons = { "●", "○", "◆", "◇" } },
			checkbox = {
				checked = { icon = "󰄲 " },
				unchecked = { icon = "󰄱 " },
			},
		},
		keys = {
			{ "<leader>mr", "<cmd>RenderMarkdown toggle<CR>", ft = "markdown", desc = "Toggle markdown rendering" },
			{ "<leader>mp", glow_preview, ft = "markdown", desc = "Preview markdown with glow" },
			{ "<leader>mP", glow_tmux_split, ft = "markdown", desc = "Preview markdown in tmux split" },
		},
	},
}
