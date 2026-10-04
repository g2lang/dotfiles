"""Regression test using real insert-mode input, not just a startup check.

Run: python3 tests/test_nvim_completion.py
Requires nvim, pynvim, and the configured plugins already installed by Lazy.
Uses the repository config without rebuilding Home Manager; writes no documents.
"""

import os
from pathlib import Path
import time

import pynvim


repo = Path(__file__).resolve().parents[1]
os.environ["XDG_CONFIG_HOME"] = str(repo / ".config")
nvim = pynvim.attach("child", argv=["nvim", "--embed", "--headless", "-n"])
try:
    nvim.ui_attach(100, 30, rgb=True)
    nvim.exec_lua('require("lazy").load({ plugins = { "blink.cmp" } })')

    for filetype in ("markdown", "gitcommit"):
        nvim.command("enew!")
        nvim.command(f"setfiletype {filetype}")
        assert nvim.exec_lua('return require("blink.cmp.config").enabled()') is False
        # Seed a tempting buffer completion, then type the reported problem words.
        nvim.current.buffer[:] = ["commands", ""]
        nvim.current.window.cursor = (2, 0)
        nvim.input("i")
        for word in ("commits", "Setup"):
            nvim.input(word)
            time.sleep(0.5)
            assert not nvim.exec_lua('return require("blink.cmp").is_visible()')
            nvim.input("<CR>")
            time.sleep(0.1)
        nvim.input("<Tab>text<Esc>")
        time.sleep(0.1)
        lines = nvim.current.buffer[:]
        assert lines[:3] == ["commands", "commits", "Setup"], lines
        assert len(lines) == 4 and lines[3].lstrip() == "text" and lines[3][0].isspace(), lines
        assert nvim.current.window.options["spell"]
        print(f"PASS: {filetype}: Enter/Tab preserve typed words; spelling stays enabled")

    # Check the same instance does not remain disabled after switching to code.
    for filetype in ("rust", "python"):
        nvim.command("enew!")
        # Avoid starting external language servers; exercise Blink's filetype gate.
        nvim.command(f"noautocmd setlocal filetype={filetype}")
        assert nvim.exec_lua('return require("blink.cmp.config").enabled()') is True
        print(f"PASS: {filetype}: completion remains enabled")
finally:
    try:
        nvim.command("qa!")
    except EOFError:
        pass
    nvim.close()
