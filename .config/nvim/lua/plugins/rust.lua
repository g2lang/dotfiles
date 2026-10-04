return {
	{
		"mrcjkb/rustaceanvim",
		version = "^6",
		lazy = false,
		init = function()
			vim.g.rustaceanvim = {
				tools = {
					hover_actions = { auto_focus = true },
					float_win_config = { border = "rounded" },
				},
				server = {
					default_settings = {
						["rust-analyzer"] = {
							cargo = {
								allFeatures = true,
								buildScripts = { enable = true },
							},
							check = {
								command = "clippy",
								allTargets = true,
							},
							completion = {
								callable = { snippets = "add_parentheses" },
								postfix = { enable = true },
							},
							imports = {
								granularity = { group = "module" },
								prefix = "self",
							},
							inlayHints = {
								bindingModeHints = { enable = true },
								closureReturnTypeHints = { enable = "always" },
								lifetimeElisionHints = { enable = "always", useParameterNames = true },
								typeHints = { enable = true },
							},
							procMacro = { enable = true },
						},
					},
				},
			}
		end,
		keys = {
			{ "<leader>rr", "<cmd>RustLsp runnables<CR>", desc = "Rust runnables" },
			{ "<leader>rt", "<cmd>RustLsp testables<CR>", desc = "Rust testables" },
			{ "<leader>rd", "<cmd>RustLsp debuggables<CR>", desc = "Rust debuggables" },
			{ "<leader>re", "<cmd>RustLsp explainError<CR>", desc = "Explain Rust error" },
			{ "<leader>rE", "<cmd>RustLsp renderDiagnostic<CR>", desc = "Render Rust diagnostic" },
			{ "<leader>rm", "<cmd>RustLsp expandMacro<CR>", desc = "Expand Rust macro" },
			{ "<leader>rp", "<cmd>RustLsp parentModule<CR>", desc = "Rust parent module" },
			{ "<leader>rC", "<cmd>RustLsp openCargo<CR>", desc = "Open Cargo.toml" },
			{ "<leader>ca", "<cmd>RustLsp codeAction<CR>", ft = "rust", desc = "Rust code action" },
			{ "K", "<cmd>RustLsp hover actions<CR>", ft = "rust", desc = "Rust hover actions" },
		},
	},

	{
		"saecki/crates.nvim",
		event = { "BufRead Cargo.toml" },
		dependencies = { "nvim-lua/plenary.nvim" },
		opts = {
			completion = { crates = { enabled = true } },
			lsp = { enabled = true, actions = true, completion = true, hover = true },
		},
		keys = {
			{
				"<leader>ct",
				function()
					require("crates").toggle()
				end,
				ft = "toml",
				desc = "Toggle crates info",
			},
			{
				"<leader>cu",
				function()
					require("crates").upgrade_crate()
				end,
				ft = "toml",
				desc = "Upgrade crate",
			},
			{
				"<leader>cU",
				function()
					require("crates").upgrade_all_crates()
				end,
				ft = "toml",
				desc = "Upgrade all crates",
			},
		},
	},
}
