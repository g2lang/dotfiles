return {
	{
		"saghen/blink.cmp",
		version = "1.*",
		event = "InsertEnter",
		dependencies = { "rafamadriz/friendly-snippets" },
		opts = {
			-- Disable completion and its accept/snippet keymaps in prose buffers.
			-- Blink's context has no `filetype` field; read the buffer option instead.
			enabled = function()
				local ft = vim.bo.filetype
				return ft ~= "markdown" and ft ~= "gitcommit"
			end,
			keymap = { preset = "enter" },
			appearance = {
				nerd_font_variant = "mono",
			},
			completion = {
				documentation = { auto_show = true, auto_show_delay_ms = 250 },
				ghost_text = { enabled = true },
				menu = { border = "rounded" },
			},
			signature = { enabled = true, window = { border = "rounded" } },
			snippets = { preset = "default" },
			sources = {
				default = { "lsp", "path", "snippets", "buffer" },
			},
		},
	},

	{
		"folke/lazydev.nvim",
		ft = "lua",
		opts = {
			library = {
				{ path = "luvit-meta/library", words = { "vim%.uv" } },
			},
		},
	},

	{
		"neovim/nvim-lspconfig",
		event = { "BufReadPre", "BufNewFile" },
		dependencies = {
			"saghen/blink.cmp",
			"folke/lazydev.nvim",
		},
		config = function()
			vim.diagnostic.config({
				virtual_text = { spacing = 4, prefix = "●" },
				severity_sort = true,
				float = { border = "rounded", source = "if_many" },
				signs = {
					text = {
						[vim.diagnostic.severity.ERROR] = " ",
						[vim.diagnostic.severity.WARN] = " ",
						[vim.diagnostic.severity.INFO] = " ",
						[vim.diagnostic.severity.HINT] = "󰌵 ",
					},
				},
			})

			local capabilities = require("blink.cmp").get_lsp_capabilities()

			vim.api.nvim_create_autocmd("LspAttach", {
				group = vim.api.nvim_create_augroup("UserLspConfig", { clear = true }),
				callback = function(event)
					local client = vim.lsp.get_client_by_id(event.data.client_id)
					local bufnr = event.buf
					local map = function(mode, lhs, rhs, desc)
						vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, silent = true, desc = desc })
					end

					if client and client.name == "ruff" then
						-- Prefer basedpyright for hover/signature help and ruff for lint/code actions.
						client.server_capabilities.hoverProvider = false
					end

					map("n", "gd", vim.lsp.buf.definition, "Go to definition")
					map("n", "gD", vim.lsp.buf.declaration, "Go to declaration")
					map("n", "gr", vim.lsp.buf.references, "References")
					map("n", "gI", vim.lsp.buf.implementation, "Go to implementation")
					map("n", "gy", vim.lsp.buf.type_definition, "Go to type definition")
					map("n", "K", vim.lsp.buf.hover, "Hover")
					map("n", "<C-k>", vim.lsp.buf.signature_help, "Signature help")
					map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, "Code action")
					map("n", "<leader>cr", vim.lsp.buf.rename, "Rename")
					map("n", "<leader>wa", vim.lsp.buf.add_workspace_folder, "Add workspace folder")
					map("n", "<leader>wr", vim.lsp.buf.remove_workspace_folder, "Remove workspace folder")
					map("n", "<leader>wl", function()
						print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
					end, "List workspace folders")

					if client and client.server_capabilities.inlayHintProvider and vim.lsp.inlay_hint then
						vim.lsp.inlay_hint.enable(true, { bufnr = bufnr })
						map("n", "<leader>th", function()
							vim.lsp.inlay_hint.enable(
								not vim.lsp.inlay_hint.is_enabled({ bufnr = bufnr }),
								{ bufnr = bufnr }
							)
						end, "Toggle inlay hints")
					end
				end,
			})

			local servers = {
				basedpyright = {
					settings = {
						basedpyright = {
							analysis = {
								autoSearchPaths = true,
								diagnosticMode = "workspace",
								typeCheckingMode = "standard",
								useLibraryCodeForTypes = true,
							},
						},
					},
				},
				ruff = {
					init_options = {
						settings = {
							lint = { enable = true },
							format = { preview = true },
						},
					},
				},
				marksman = {},
				typos_lsp = {},
				nixd = {
					settings = {
						nixd = {
							formatting = { command = { "nixfmt" } },
							options = {
								nixos = {
									expr = "(builtins.getFlake (builtins.toString ./.)).nixosConfigurations.dev-laptop.options",
								},
								home_manager = {
									expr = "(builtins.getFlake (builtins.toString ./.)).nixosConfigurations.dev-laptop.options.home-manager.users.type.getSubOptions []",
								},
							},
						},
					},
				},
				taplo = {},
				bashls = {},
				yamlls = {},
				jsonls = {},
				lua_ls = {
					settings = {
						Lua = {
							completion = { callSnippet = "Replace" },
							diagnostics = { globals = { "vim" } },
							hint = { enable = true },
							telemetry = { enable = false },
							workspace = { checkThirdParty = false },
						},
					},
				},
			}

			for server, config in pairs(servers) do
				config.capabilities = vim.tbl_deep_extend("force", {}, capabilities, config.capabilities or {})
				vim.lsp.config(server, config)
				vim.lsp.enable(server)
			end
		end,
	},
}
