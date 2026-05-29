#!/usr/bin/env python3
"""
examples/main.py — unified runner for all LangGraph design-pattern examples.

Usage
-----
    python examples/main.py list
    python examples/main.py run 00 "Hello, world!"
    python examples/main.py run 01 "What is LangGraph?"

    # Use a local Ollama endpoint instead of OpenAI
    python examples/main.py --openai-base-url http://localhost:11434/v1 \\
                            --openai-api-key ollama \\
                            --openai-model llama3.2 \\
                            run 01 "Hello"

    # Load credentials from a .env file
    python examples/main.py --env-file .env run 05 "remember: I like coffee"

    # Specify user / thread IDs for stateful examples
    python examples/main.py run 04 "Hi" --thread-id my-session
    python examples/main.py run 07 "Check order 99887" --user-id alice --thread-id alice-session
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import types
from pathlib import Path
from typing import Any

EXAMPLES_DIR = Path(__file__).parent

# ── Registry ──────────────────────────────────────────────────────────────────
# Describes every example so main.py can drive it without touching each file.
#
#   dir          – sub-directory name (may contain hyphens)
#   description  – one-liner shown by `list`
#   input_type   – "user_query" | "messages"
#   output_key   – state key to print; "messages" means last message content
#   has_context  – graph was built with context_schema=Context(user_id=…)
#   has_thread   – graph uses InMemorySaver (needs thread_id in config)

REGISTRY: dict[str, dict[str, Any]] = {
    "00": {
        "dir": "00-hello-stategraph",
        "description": "Hello StateGraph — pure Python, no LLM",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": False,
        "has_thread": False,
    },
    "01": {
        "dir": "01-llm-call",
        "description": "Single LLM call",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": False,
        "has_thread": False,
    },
    "02": {
        "dir": "02-tools-basics",
        "description": "Tool gating (order lookup)",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": False,
        "has_thread": False,
    },
    "03": {
        "dir": "03-router",
        "description": "LLM-based router to multiple branches",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": False,
        "has_thread": False,
    },
    "03b": {
        "dir": "03b-rag-branch",
        "description": "Router + RAG branch",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": False,
        "has_thread": False,
    },
    "04": {
        "dir": "04-short-term-memory",
        "description": "Short-term memory via InMemorySaver checkpointer",
        "input_type": "messages",
        "output_key": "messages",
        "has_context": False,
        "has_thread": True,
    },
    "05": {
        "dir": "05-long-term-memory-store",
        "description": "Long-term memory via InMemoryStore",
        "input_type": "user_query",
        "output_key": "answer",
        "has_context": True,
        "has_thread": False,
    },
    "06": {
        "dir": "06-context-window-summarize",
        "description": "Context-window summarization",
        "input_type": "messages",
        "output_key": "messages",
        "has_context": False,
        "has_thread": False,
    },
    "07": {
        "dir": "07-capstone-support-agent",
        "description": "Capstone: routing + memory + tools",
        "input_type": "messages",
        "output_key": "answer",
        "has_context": True,
        "has_thread": True,
    },
}


# ── Dynamic module loader ─────────────────────────────────────────────────────

def _load_example(example_dir: str) -> types.ModuleType:
    """
    Load graph.py from an example sub-directory, respecting relative imports.

    Directory names with hyphens (e.g. "01-llm-call") are not valid Python
    identifiers, so we register a synthetic package in sys.modules and load
    each source file manually in dependency order.
    """
    dir_path = EXAMPLES_DIR / example_dir
    pkg_name = "_ex_" + example_dir.replace("-", "_").replace(".", "_")

    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [str(dir_path)]  # type: ignore[assignment]
        pkg.__package__ = pkg_name
        pkg.__file__ = str(dir_path / "__init__.py")
        sys.modules[pkg_name] = pkg

    def _load_file(filename: str) -> types.ModuleType | None:
        fpath = dir_path / filename
        if not fpath.exists():
            return None
        mod_name = f"{pkg_name}.{filename[:-3]}"
        if mod_name in sys.modules:
            return sys.modules[mod_name]
        spec = importlib.util.spec_from_file_location(mod_name, fpath)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = pkg_name
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod

    for fname in ("state.py", "llm.py", "tools.py", "nodes.py", "graph.py"):
        _load_file(fname)

    return sys.modules[f"{pkg_name}.graph"]


# ── State / output helpers ────────────────────────────────────────────────────

def _build_initial_state(meta: dict, user_input: str) -> dict:
    if meta["input_type"] == "messages":
        from langchain_core.messages import HumanMessage
        return {"messages": [HumanMessage(content=user_input)]}
    return {"user_query": user_input}


def _extract_output(meta: dict, result: dict) -> str:
    if meta["output_key"] == "messages":
        messages = result.get("messages", [])
        if messages:
            last = messages[-1]
            return getattr(last, "content", str(last))
        return "(no messages in result)"

    val = result.get(meta["output_key"])
    if val is None:
        # Fallback: print all non-None fields so the user sees something useful
        non_null = {k: v for k, v in result.items() if v is not None}
        return str(non_null) if non_null else "(no output)"
    return str(val)


# ── Subcommand handlers ───────────────────────────────────────────────────────

def cmd_list(_args: argparse.Namespace) -> None:
    print("Available examples:\n")
    for key, meta in REGISTRY.items():
        flags = []
        if meta["has_context"]:
            flags.append("context")
        if meta["has_thread"]:
            flags.append("thread")
        flag_str = f"  [{', '.join(flags)}]" if flags else ""
        print(f"  {key:<5s}  {meta['dir']:<35s}  {meta['description']}{flag_str}")
    print(
        "\nFlags: [context] = needs --user-id, [thread] = needs --thread-id\n"
        "       Both default to 'demo-user' / 'demo-thread'."
    )


def cmd_run(args: argparse.Namespace) -> None:
    example_id = args.example
    meta = REGISTRY[example_id]
    user_input: str = args.input

    print(f"Running example {example_id}: {meta['description']}")
    print(f"Input: {user_input!r}\n")

    graph_mod = _load_example(meta["dir"])
    app = graph_mod.build_graph()

    state = _build_initial_state(meta, user_input)

    config: dict = {}
    if meta["has_thread"]:
        config["configurable"] = {"thread_id": args.thread_id}

    context = None
    if meta["has_context"]:
        pkg_name = "_ex_" + meta["dir"].replace("-", "_").replace(".", "_")
        state_mod = sys.modules.get(f"{pkg_name}.state")
        if state_mod and hasattr(state_mod, "Context"):
            context = state_mod.Context(user_id=args.user_id)

    invoke_kwargs: dict[str, Any] = {}
    if config:
        invoke_kwargs["config"] = config
    if context is not None:
        invoke_kwargs["context"] = context

    result = app.invoke(state, **invoke_kwargs)

    output = _extract_output(meta, result)
    print("Output:")
    print(output)


# ── CLI wiring ────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python examples/main.py",
        description="Run LangGraph design-pattern examples from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Global options — applied before any example module is imported so that
    # env vars are visible to get_llm() when it runs.
    parser.add_argument(
        "--env-file",
        metavar="PATH",
        default=None,
        help=(
            "Path to a .env file to load (default: .env next to this file, "
            "if it exists)."
        ),
    )
    parser.add_argument(
        "--openai-base-url",
        metavar="URL",
        help="Override OPENAI_BASE_URL (e.g. http://localhost:11434/v1 for Ollama).",
    )
    parser.add_argument(
        "--openai-api-key",
        metavar="KEY",
        help="Override OPENAI_API_KEY.",
    )
    parser.add_argument(
        "--openai-model",
        metavar="MODEL",
        help="Override OPENAI_MODEL.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all available examples.")

    run_p = sub.add_parser("run", help="Run an example graph.")
    run_p.add_argument(
        "example",
        choices=sorted(REGISTRY),
        metavar="EXAMPLE",
        help=f"Which example to run: {', '.join(sorted(REGISTRY))}",
    )
    run_p.add_argument(
        "input",
        nargs="?",
        default="Hello, world!",
        help="User input passed into the graph (default: 'Hello, world!').",
    )
    run_p.add_argument(
        "--user-id",
        default="demo-user",
        metavar="ID",
        help="User ID injected as Context for examples 05 and 07 (default: demo-user).",
    )
    run_p.add_argument(
        "--thread-id",
        default="demo-thread",
        metavar="ID",
        help="Thread ID for checkpointer-enabled examples 04 and 07 (default: demo-thread).",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    # ── 1. Load .env ──────────────────────────────────────────────────────────
    env_path = Path(args.env_file) if args.env_file else EXAMPLES_DIR.parent / ".env"
    try:
        from dotenv import load_dotenv

        if env_path.exists():
            load_dotenv(env_path, override=False)
    except ImportError:
        if args.env_file and env_path.exists():
            print(
                f"Warning: python-dotenv not installed; cannot load {env_path}",
                file=sys.stderr,
            )

    # ── 2. Apply CLI overrides ─────────────────────────────────────────────────
    # CLI flags take precedence over .env / existing env vars.
    if args.openai_base_url:
        os.environ["OPENAI_BASE_URL"] = args.openai_base_url
    if args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if args.openai_model:
        os.environ["OPENAI_MODEL"] = args.openai_model

    # ── 3. Dispatch ───────────────────────────────────────────────────────────
    if args.command == "list":
        cmd_list(args)
    elif args.command == "run":
        cmd_run(args)


if __name__ == "__main__":
    main()
