return {
	{
		"catppuccin/nvim",
		name = "catppuccin",
		lazy = false,
		priority = 1000,
		opts = {
			flavour = "mocha",
			integrations = {
				blink_cmp = true,
				gitsigns = true,
				markdown = true,
				native_lsp = { enabled = true },
				telescope = { enabled = true },
				treesitter = true,
				which_key = true,
			},
		},
		config = function(_, opts)
			require("catppuccin").setup(opts)
			vim.cmd.colorscheme("catppuccin")
		end,
	},

	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {
			preset = "modern",
			delay = 350,
			spec = {
				{ "<leader>b", group = "buffers" },
				{ "<leader>c", group = "code" },
				{ "<leader>d", group = "debug" },
				{ "<leader>f", group = "find/files" },
				{ "<leader>g", group = "git" },
				{ "<leader>m", group = "markdown" },
				{ "<leader>r", group = "rust/run" },
				{ "<leader>s", group = "search" },
				{ "<leader>t", group = "tests/toggles" },
				{ "<leader>w", group = "workspace" },
			},
		},
	},

	{
		"nvim-lualine/lualine.nvim",
		lazy = false,
		dependencies = { "nvim-tree/nvim-web-devicons" },
		config = function()
			require("lualine").setup({
				options = {
					-- Use the exact Catppuccin lualine theme name provided by the
					-- Catppuccin plugin to avoid theme-resolution notices.
					theme = "catppuccin-mocha",
					globalstatus = true,
					component_separators = "",
					section_separators = { left = "", right = "" },
				},
				sections = {
					lualine_c = {
						{ "filename", path = 1 },
					},
					lualine_x = { "diagnostics", "encoding", "filetype" },
				},
			})

			local show_lualine_notices = function()
				require("lualine.utils.notices").show_notices()
			end
			-- Lualine normally only defines `:LualineNotices` when it has notices.
			-- Define it unconditionally, plus the common `:LuaLineNotices` spelling.
			vim.api.nvim_create_user_command("LualineNotices", show_lualine_notices, { force = true })
			vim.api.nvim_create_user_command("LuaLineNotices", show_lualine_notices, { force = true })
		end,
	},

	{
		"lewis6991/gitsigns.nvim",
		event = { "BufReadPre", "BufNewFile" },
		opts = {
			current_line_blame = false,
			on_attach = function(bufnr)
				local gs = package.loaded.gitsigns
				local map = function(mode, lhs, rhs, desc, extra_opts)
					vim.keymap.set(
						mode,
						lhs,
						rhs,
						vim.tbl_extend("force", { buffer = bufnr, desc = desc }, extra_opts or {})
					)
				end

				map("n", "]h", function()
					if vim.wo.diff then
						return "]h"
					end
					vim.schedule(gs.next_hunk)
					return "<Ignore>"
				end, "Next git hunk", { expr = true })
				map("n", "[h", function()
					if vim.wo.diff then
						return "[h"
					end
					vim.schedule(gs.prev_hunk)
					return "<Ignore>"
				end, "Previous git hunk", { expr = true })
				map("n", "<leader>gp", gs.preview_hunk, "Preview hunk")
				map("n", "<leader>gr", gs.reset_hunk, "Reset hunk")
				map("v", "<leader>gr", function()
					gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") })
				end, "Reset hunk")
				map("n", "<leader>gb", gs.blame_line, "Blame line")
			end,
		},
	},

	{
		"folke/todo-comments.nvim",
		event = { "BufReadPost", "BufNewFile" },
		dependencies = { "nvim-lua/plenary.nvim" },
		opts = {},
		keys = {
			{
				"]t",
				function()
					require("todo-comments").jump_next()
				end,
				desc = "Next todo comment",
			},
			{
				"[t",
				function()
					require("todo-comments").jump_prev()
				end,
				desc = "Previous todo comment",
			},
			{ "<leader>st", "<cmd>TodoTelescope<CR>", desc = "Todo comments" },
		},
	},

	{
		"echasnovski/mini.nvim",
		version = false,
		event = "VeryLazy",
		config = function()
			require("mini.ai").setup({ n_lines = 500 })
			require("mini.comment").setup()
			require("mini.pairs").setup()
			require("mini.surround").setup()
			require("mini.trailspace").setup()
		end,
	},
}
