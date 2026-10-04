return {
	{
		"stevearc/conform.nvim",
		event = { "BufWritePre" },
		cmd = { "ConformInfo" },
		keys = {
			{
				"<leader>cf",
				function()
					require("conform").format({ async = true, lsp_format = "fallback" })
				end,
				mode = { "n", "v" },
				desc = "Format buffer/range",
			},
		},
		opts = {
			notify_on_error = false,
			format_on_save = function(bufnr)
				local disable_filetypes = { c = true, cpp = true }
				if disable_filetypes[vim.bo[bufnr].filetype] then
					return nil
				end
				return { timeout_ms = 2500, lsp_format = "fallback" }
			end,
			formatters_by_ft = {
				rust = { "rustfmt" },
				python = { "ruff_fix", "ruff_organize_imports", "ruff_format" },
				markdown = { "prettierd", "prettier", stop_after_first = true },
				lua = { "stylua" },
				nix = { "nixfmt" },
				sh = { "shfmt" },
				bash = { "shfmt" },
				zsh = { "shfmt" },
				toml = { "taplo" },
				yaml = { "prettierd", "prettier", stop_after_first = true },
				json = { "prettierd", "prettier", stop_after_first = true },
				jsonc = { "prettierd", "prettier", stop_after_first = true },
			},
		},
	},

	{
		"mfussenegger/nvim-lint",
		event = { "BufReadPost", "BufNewFile" },
		config = function()
			local lint = require("lint")

			-- Keep prose linting useful without flagging intentional breathing room in
			-- notes/docs. The config also disables hard line-length checks; wrapping is
			-- an editor/view concern for this setup.
			lint.linters["markdownlint-cli2"].args = {
				"--config",
				vim.fn.stdpath("config") .. "/markdownlint.json",
				"-",
			}

			lint.linters_by_ft = {
				python = { "ruff" },
				-- Vale is installed for projects that opt into it, but it exits noisily
				-- without a project/user Vale config. Typos are handled by typos-lsp.
				markdown = { "markdownlint-cli2" },
				sh = { "shellcheck" },
				bash = { "shellcheck" },
				zsh = { "shellcheck" },
				nix = { "statix", "deadnix" },
			}

			local group = vim.api.nvim_create_augroup("UserLint", { clear = true })
			vim.api.nvim_create_autocmd({ "BufEnter", "BufWritePost", "InsertLeave" }, {
				group = group,
				callback = function()
					lint.try_lint()
				end,
			})

			vim.keymap.set("n", "<leader>cl", function()
				lint.try_lint()
			end, { desc = "Lint current file" })
		end,
	},
}
