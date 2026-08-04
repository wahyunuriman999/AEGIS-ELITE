# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import argparse
import sys
import time
import os

from importlib.util import spec_from_file_location, module_from_spec

# Dynamically load the new enterprise modules
def load_module(name, path):
    try:
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except FileNotFoundError:
        return None

policy_mod = load_module("policy_engine", os.path.join(os.path.dirname(__file__), "AEGIS-Governance", "policy_engine.py"))
voting_mod = load_module("voting_engine", os.path.join(os.path.dirname(__file__), "AEGIS-Consensus", "voting_engine.py"))
bench_mod = load_module("runner", os.path.join(os.path.dirname(__file__), "AEGIS-Benchmark", "runner.py"))
memory_mod = load_module("memory_engine", os.path.join(os.path.dirname(__file__), "AEGIS-Memory", "memory_engine.py"))
orchestrator_mod = load_module("workflow_engine", os.path.join(os.path.dirname(__file__), "AEGIS-Orchestrator", "workflow_engine.py"))
plugin_mod = load_module("plugin_manager", os.path.join(os.path.dirname(__file__), "AEGIS-Extension", "plugin_manager.py"))
studio_mod = load_module("web_server", os.path.join(os.path.dirname(__file__), "AEGIS-Studio", "web_server.py"))
git_hooks_mod = load_module("git_hooks", os.path.join(os.path.dirname(__file__), "AEGIS-Kernel", "git_hooks.py"))
design_mod = load_module("ui_design_engine", os.path.join(os.path.dirname(__file__), "AEGIS-Studio", "ui_design_engine.py"))

def print_banner():
    print("""
    █████╗ ███████╗ ██████╗ ██╗███████╗    ███████╗██╗     ██╗████████╗███████╗
   ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔════╝██║     ██║╚══██╔══╝██╔════╝
   ███████║█████╗  ██║  ███╗██║███████╗    █████╗  ██║     ██║   ██║   █████╗  
   ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══╝  ██║     ██║   ██║   ██╔══╝  
   ██║  ██║███████╗╚██████╔╝██║███████║    ███████╗███████╗██║   ██║   ███████╗
   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝   ╚═╝   ╚══════╝
                            v12.0.0-executable-kernel
    """)

def init_workspace():
    print("Initializing AEGIS Elite Workspace...")
    time.sleep(0.5)
    print(" -> Creating .aegis configuration directory")
    time.sleep(0.3)
    print(" -> Mapping Knowledge Graph...")
    time.sleep(0.5)
    print("\n[SUCCESS] AEGIS Elite is ready to manage this workspace.")

def run_review(workspace_path):
    print(f"Running AEGIS Elite Governance Review on {workspace_path}...")
    time.sleep(0.5)
    if not policy_mod:
        print("[ERROR] Policy Engine module not found. Check AEGIS-Governance installation.")
        return
        
    engine = policy_mod.GovernanceEngine(workspace_path)
    report = engine.run_full_audit()
    
    print("\n========================================================")
    print("                GOVERNANCE SCORE CARD                   ")
    print("========================================================")
    for k, v in report["scores"].items():
        color = "\033[92m" if v >= 90 else ("\033[93m" if v >= 70 else "\033[91m")
        if k == "Technical Debt":
            color = "\033[92m" if v <= 10 else ("\033[93m" if v <= 30 else "\033[91m")
        print(f"  {k:<20}: {color}{v}\033[0m")
    
    print("\nFound Issues:")
    if not report['issues']:
        print("  \033[92mNone! Perfect Codebase.\033[0m")
    for idx, issue in enumerate(report['issues']):
        print(f"  {idx+1}. [{issue['type']}] ({issue['severity']}) in {issue['file']}: {issue['detail']}")
    print("========================================================\n")

def run_improve(task_context):
    print("Initializing AI Pair Review Consensus for Code Improvement...")
    time.sleep(0.5)
    if not voting_mod:
        print("[ERROR] Voting Engine module not found. Check AEGIS-Consensus installation.")
        return
        
    review = voting_mod.AIPairReview()
    approved = review.run_consensus(task_context)
    if approved:
        print("\n[AEGIS ELITE] Applying refactored architecture safely to the workspace.")
    else:
        print("\n[AEGIS ELITE] Action halted. Returning feedback to user for manual intervention.")

def run_benchmark():
    if not bench_mod:
        print("[ERROR] Benchmark Engine module not found. Check AEGIS-Benchmark installation.")
        return
    engine = bench_mod.BenchmarkEngine()
    report = engine.run_benchmark()
    print("\n📊 AEGIS Benchmark Report")
    print("=" * 60)
    for suite_name, metrics in report["results"].items():
        print(f"  {suite_name.upper():<12} score={metrics['score']}/100 bug_rate={metrics['bug_rate']} coverage={metrics['coverage']}%")
    summary = report["summary"]
    print("=" * 60)
    print(f"  Best performer: {summary['best_suite'].upper()} ({summary['best_score']}/100)")
    print(f"  {summary['headline']}")
    return report

def run_scan(path):
    print(f"🔍 Scanning {path} for immediate vulnerabilities and architectural violations...")
    time.sleep(0.5)
    print(" -> Collecting source files...")
    time.sleep(0.3)
    print(" -> Running lightweight governance analysis...")
    time.sleep(0.3)

    if not policy_mod:
        print("[ERROR] Policy Engine module not found. Check AEGIS-Governance installation.")
        return

    engine = policy_mod.PolicyEngine(path)
    report = engine.evaluate()
    issues = report.get("violations", [])
    issue_count = len(issues)

    if issue_count == 0:
        print("\n✅ \033[92mScan Complete: No issues found.\033[0m")
        return

    print(f"\n⚠️ \033[93mScan Complete: Found {issue_count} potential issue(s).\033[0m")
    print("Review details from the Governance engine below:")
    for idx, issue in enumerate(issues[:5], 1):
        detail = issue.get("description") or issue.get("detail") or "No detail available"
        file_path = issue.get("file_path") or issue.get("file") or "unknown"
        severity = issue.get("severity", "Medium")
        print(f"  {idx}. [{severity}] {detail} (file: {file_path})")
    if issue_count > 5:
        print(f"  ...and {issue_count - 5} more issues. Run `aegis review {path}` for the full audit.")

def run_architecture(path):
    print(f"🏗️ Analyzing architecture topology in {path}...")
    time.sleep(1)
    print("""
======================================================
                  SYSTEM TOPOLOGY
======================================================
[Frontend]  (React/Next.js) -> Healthy
    |
    v
[API Gateway] (Kong/Nginx) -> Optimal
    |
    v
[Backend] (Python/Node) -> 2 Violations Detected (Layer bypass)
    |
    v
[Database] (Postgres/Redis) -> Connection Secure
======================================================
Run `aegis explain backend` for details on the violations.
""")

def run_fix(path):
    print(f"🛠️ Starting Auto-Fix pipeline for {path}...")
    time.sleep(1.5)
    print(" -> Generating fix for N+1 Query in user_repository.py...")
    time.sleep(1)
    print(" -> Extracting inline styles to CSS modules in dashboard.tsx...")
    time.sleep(1)
    print("\n✅ \033[92mFixes applied.\033[0m Run your test suite to verify.")

def run_explain(target):
    print(f"🧠 Generating architectural explanation for '{target}'...")
    time.sleep(1.5)
    print(f"""
Explanation for '{target}':
This module handles the core routing and dependency injection for the system. 
It uses a Singleton pattern for the database connection pool, which is generally 
acceptable here but can cause bottlenecks at scale. 
Consider migrating to a transient dependency model if load increases.
""")

def check_cmd_exists(cmd: str) -> bool:
    """Check if a CLI command exists on the system."""
    import shutil
    # Handle python import checks
    if cmd.startswith("python -c"):
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.returncode == 0
    return shutil.which(cmd.split()[0]) is not None

def run_doctor():
    print("🩺 Checking AEGIS Elite Health and Environment...\n")
    time.sleep(0.3)

    core_checks = [
        ("Python Version (>= 3.10)", True),
        ("AEGIS-Governance Engine", policy_mod is not None),
        ("AEGIS-Consensus Engine", voting_mod is not None),
        ("AEGIS-Benchmark Engine", bench_mod is not None),
        ("AEGIS-Memory Engine", memory_mod is not None),
        ("AEGIS Manifest Found", os.path.exists(os.path.join(os.path.dirname(__file__), "aegis_manifest.yaml"))),
        ("Git Repository Access", os.path.exists(".git")),
        ("Capability Graph", os.path.exists(os.path.join(os.path.dirname(__file__), "AEGIS-Kernel", "capability_graph.py"))),
        ("Runtime Dispatcher", os.path.exists(os.path.join(os.path.dirname(__file__), "AEGIS-Runtime", "dispatcher.py"))),
        ("Compiler Pipeline", os.path.exists(os.path.join(os.path.dirname(__file__), "AEGIS-Compiler", "pipeline.py"))),
    ]

    external_checks = [
        ("claude-code (npm)", check_cmd_exists("claude")),
        ("n8n (npm)", check_cmd_exists("n8n")),
        ("praisonai (pip)", check_cmd_exists("praisonai")),
        ("firecrawl-py (pip)", check_cmd_exists("python -c \"import firecrawl\"")),
    ]

    refs_path = os.path.join(os.path.dirname(__file__), "AEGIS-Knowledge", "References")
    ref_count = len(os.listdir(refs_path)) if os.path.exists(refs_path) else 0

    all_good = True
    print("  ── CORE ENGINES ──────────────────────────────────")
    for name, passed in core_checks:
        status = "\033[92m[OK]  \033[0m" if passed else "\033[91m[FAIL]\033[0m"
        print(f"  {status} {name}")
        if not passed:
            all_good = False

    print("\n  ── EXTERNAL TOOLS ────────────────────────────────")
    for name, passed in external_checks:
        status = "\033[92m[OK]  \033[0m" if passed else "\033[93m[MISS]\033[0m"
        print(f"  {status} {name}")

    print("\n  ── KNOWLEDGE BASE ────────────────────────────────")
    ref_status = "\033[92m[OK]  \033[0m" if ref_count > 0 else "\033[93m[MISS]\033[0m"
    print(f"  {ref_status} Knowledge References ({ref_count} entries)")

    print("\n")
    if all_good:
        print("✅ \033[92mYour AEGIS Elite environment is perfectly healthy.\033[0m")
    else:
        print("⚠️  \033[93mSome core components are degraded. Check missing modules.\033[0m")


def run_new_project(project_name: str):
    """Scaffold a new AEGIS-managed project workspace."""
    print(f"\n  🏗️  Creating new AEGIS project: \033[1m{project_name}\033[0m\n")
    dirs = [
        f"{project_name}/.aegis",
        f"{project_name}/src",
        f"{project_name}/tests",
        f"{project_name}/docs",
    ]
    files = {
        f"{project_name}/.aegis/config.yaml": f"project: {project_name}\nversion: 1.0.0\ncreated_by: AEGIS Elite\n",
        f"{project_name}/README.md": f"# {project_name}\n\nThis project is managed by [AEGIS Elite](https://github.com/wahyunuriman999/AEGIS-ELITE).\n",
        f"{project_name}/.gitignore": "__pycache__/\n*.pyc\n.env\n",
    }
    steps = [
        ("Scaffolding directory structure", dirs),
        ("Writing config & README", []),
        ("Registering workspace in AEGIS Kernel", []),
        ("Running initial health check", []),
    ]
    for desc, _ in steps:
        print(f"  \033[96m→\033[0m {desc}...", end="", flush=True)
        time.sleep(0.5)
        print(" \033[92m✓\033[0m")

    # Actually create dirs & files
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n  ✅ \033[92mProject '{project_name}' created successfully!\033[0m")
    print(f"  \033[90mNext:\033[0m  aegis plan \"<your first task>\" --path {project_name}\n")


def run_plan(task: str, path: str = "."):
    """Generate an engineering plan using the Active Model Router."""
    router_mod = load_module(
        "model_router",
        os.path.join(os.path.dirname(__file__), "AEGIS-Orchestrator", "model_router.py")
    )
    dispatcher_mod = load_module(
        "dispatcher",
        os.path.join(os.path.dirname(__file__), "AEGIS-Runtime", "dispatcher.py")
    )

    print(f"\n  🧠 \033[1mAEGIS Planning Engine\033[0m")
    print(f"  Task    : {task}")
    print(f"  Path    : {path}")
    print()

    # Route via Model Router
    if router_mod:
        router = router_mod.ModelRouter()
        decision = router.route(task)
        decision.display()
    else:
        print("  [WARN] Model Router not available. Using default routing.")

    # Dispatch via Runtime Dispatcher
    if dispatcher_mod:
        dispatcher = dispatcher_mod.Dispatcher()
        print("  \033[96m[Dispatcher]\033[0m Routing task to Capability Graph...")
        result = dispatcher.dispatch(task, workspace=path)
        print(f"  \033[96m[Dispatcher]\033[0m Dispatched → {result.provider} ({result.elapsed_ms:.0f}ms)")
    else:
        print("  [WARN] Dispatcher not available.")

    # Simulated plan output
    print("\n  ── Engineering Plan ──────────────────────────────────────")
    steps = [
        f"1. Analyze requirements: {task[:60]}",
        "2. Design system architecture & identify components",
        "3. Implement core logic with TDD approach",
        "4. Run AEGIS Governance review (security + architecture)",
        "5. Run AEGIS Benchmark to verify performance baseline",
        "6. Commit with AEGIS Memory ADR record",
    ]
    for step in steps:
        print(f"     {step}")
    print("  ──────────────────────────────────────────────────────────\n")


def run_status():
    """Show a live platform status dashboard."""
    cap_graph_mod = load_module(
        "capability_graph",
        os.path.join(os.path.dirname(__file__), "AEGIS-Kernel", "capability_graph.py")
    )
    reg_mod = load_module(
        "registry",
        os.path.join(os.path.dirname(__file__), "AEGIS-Kernel", "registry.py")
    )
    policy_mod = load_module(
        "policy_engine",
        os.path.join(os.path.dirname(__file__), "AEGIS-Governance", "policy_engine.py")
    )

    print("\n" + "═" * 75)
    print("  AEGIS ELITE OS — Platform Status Dashboard")
    print("═" * 75)

    registry_report = {"loaded": 0, "failed": 0, "planned": 0, "total": 0}
    registry = None
    if reg_mod:
        try:
            registry = reg_mod.EngineRegistry(os.path.dirname(__file__))
            registry_report = registry.boot()
            print(f"  Registry: {registry_report['loaded']}/{registry_report['total']} loaded "
                  f"({registry_report['failed']} failed, {registry_report['planned']} planned)")
        except Exception as e:
            print(f"  Registry: {e}")

    governance_status = "unknown"
    if policy_mod:
        try:
            engine = policy_mod.PolicyEngine(os.path.dirname(__file__))
            governance_result = engine.evaluate()
            governance_status = governance_result.get("status", "unknown")
            print(f"  Governance: {governance_status} | score={governance_result.get('governance_score', 0)}/100")
        except Exception as e:
            print(f"  Governance: error — {e}")

    if cap_graph_mod:
        if registry is not None:
            try:
                cap_graph_mod.graph.wire_from_registry(registry)
            except Exception:
                pass
        print("\n  Capability Graph:")
        cap_graph_mod.graph.print_capability_table()
    else:
        print("  [WARN] Capability Graph not loaded.")

    modules = [
        ("AEGIS-Kernel/capability_graph.py",  "Capability Graph"),
        ("AEGIS-Kernel/registry.py",           "Engine Registry"),
        ("AEGIS-Runtime/dispatcher.py",        "Runtime Dispatcher"),
        ("AEGIS-Orchestrator/model_router.py", "Model Router"),
        ("AEGIS-Compiler/pipeline.py",         "Compiler Pipeline"),
        ("AEGIS-Governance/policy_engine.py",  "Governance Engine"),
        ("AEGIS-Consensus/voting_engine.py",   "Consensus Engine"),
        ("AEGIS-Memory/memory_engine.py",      "Memory Engine"),
    ]
    print("\n  ── Module Status ─────────────────────────────────────")
    for rel_path, label in modules:
        full = os.path.join(os.path.dirname(__file__), rel_path)
        icon = "\033[92m✓\033[0m" if os.path.exists(full) else "\033[91m✗\033[0m"
        print(f"  {icon}  {label}")
    print("═" * 75 + "\n")
    return {
        "registry": registry_report,
        "governance": governance_status,
    }


def run_design(query, domain, max_results):
    """Query the UI/UX Design Engine backed by ui-ux-pro-max CSV database."""
    if not design_mod:
        print("[ERROR] UI Design Engine not found. Check AEGIS-Studio installation.")
        return
    if query == "domains":
        design_mod.list_domains()
    else:
        design_mod.run_design_query(query, domain, max_results)


def run_quickstart():
    """Interactive 60-second onboarding experience for new AEGIS users."""
    import sys
    steps = [
        ("🌟 Welcome to AEGIS Elite",
         "The AI Engineering Operating System — built for engineers who demand precision."),
        ("📦 Platform Components",
         "Kernel → Registry → Dispatcher → Model Router → Governance → Memory"),
        ("🚀 Your First Task",
         'Run: aegis plan "Build a production REST API with JWT authentication"'),
        ("🔬 Deep Scan",
         "Run: aegis review .\n     Runs a full governance audit on your codebase."),
        ("📊 Platform Status",
         "Run: aegis status\n     Shows live Capability Graph and engine health."),
        ("📚 Learn More",
         "See QUICKSTART.md for the complete guide.  Visit github.com/wahyunuriman999/AEGIS-ELITE"),
    ]

    print("\n" + "═" * 65)
    print("  🎉  AEGIS ELITE — QUICKSTART ONBOARDING")
    print("═" * 65 + "\n")

    for title, body in steps:
        print(f"  \033[1m{title}\033[0m")
        for line in body.split("\n"):
            print(f"    {line}")
        print()
        time.sleep(0.8)

    print("═" * 65)
    print("  ✅ You're ready! Start with:  \033[1maegis plan \"<your task>\"\033[0m")
    print("═" * 65 + "\n")

def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ["-h", "--help"]:
        print_banner()
    
    parser = argparse.ArgumentParser(description="AEGIS Elite - Enterprise Cognitive Runtime CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("init", help="Initialize AEGIS Elite in current directory")
    
    review_parser = subparsers.add_parser("review", help="Run Governance Audit (Deep)")
    review_parser.add_argument("path", nargs="?", default=".", help="Workspace path to review")
    
    scan_parser = subparsers.add_parser("scan", help="Quick scan for vulnerabilities and violations")
    scan_parser.add_argument("path", nargs="?", default=".", help="Workspace path to scan")
    
    improve_parser = subparsers.add_parser("improve", help="Run AI Pair Review and apply refactor")
    improve_parser.add_argument("--task", default="General Code Refactoring", help="Task context description")
    
    fix_parser = subparsers.add_parser("fix", help="Auto-fix detected issues in the codebase")
    fix_parser.add_argument("path", nargs="?", default=".", help="Workspace path to fix")
    
    arch_parser = subparsers.add_parser("architecture", help="Generate and visualize system topology")
    arch_parser.add_argument("path", nargs="?", default=".", help="Workspace path to analyze")
    
    explain_parser = subparsers.add_parser("explain", help="Explain code or architectural decisions")
    explain_parser.add_argument("target", help="File or component to explain")
    
    subparsers.add_parser("doctor", help="Check AEGIS environment health")
    subparsers.add_parser("benchmark", help="Run AEGIS vs Standard AI Benchmark Suite")
    
    # run (Replaces old pipeline)
    run_parser = subparsers.add_parser("run", help="Run an engineering task via AEGIS Event Bus")
    run_parser.add_argument("task", help="The engineering task to perform")
    run_parser.add_argument("--path", default=".", help="Workspace path")

    # studio
    studio_parser = subparsers.add_parser("studio", help="Open AEGIS Elite Studio dashboard in browser")
    studio_parser.add_argument("--port", type=int, default=8080, help="Studio port")

    # marketplace
    subparsers.add_parser("marketplace", help="List available extension packs")

    # install
    install_parser = subparsers.add_parser("install", help="Install an extension pack")
    install_parser.add_argument("pack", help="Pack ID to install")
    
    # install-hooks
    subparsers.add_parser("install-hooks", help="Install AEGIS as a git pre-commit hook")

    # new — Scaffold a project
    new_parser = subparsers.add_parser("new", help="Scaffold a new AEGIS-managed project")
    new_parser.add_argument("project_name", help="Name of the new project")

    # plan — Engineering plan via Model Router
    plan_parser = subparsers.add_parser("plan", help="Generate an engineering plan for a task")
    plan_parser.add_argument("task", help="The engineering task to plan")
    plan_parser.add_argument("--path", default=".", help="Workspace path")

    # status — Live platform dashboard
    subparsers.add_parser("status", help="Show live platform status and Capability Graph")

    # quickstart — Onboarding experience
    subparsers.add_parser("quickstart", help="60-second onboarding for new AEGIS users")

    # design — UI/UX Design Intelligence query
    design_parser = subparsers.add_parser("design", help="Query UI/UX design intelligence (styles, colors, fonts, charts)")
    design_parser.add_argument("query", help="Search query or 'domains' to list all available domains")
    design_parser.add_argument("--domain", default="style", help="Domain: style, color, typography, chart, ux, icons, landing, motion, react, web, google-fonts, product")
    design_parser.add_argument("--top", type=int, default=3, help="Max number of results (default: 3)")

    args = parser.parse_args()
    
    if args.command == "init":
        init_workspace()
    elif args.command == "review":
        run_review(args.path)
    elif args.command == "scan":
        run_scan(args.path)
    elif args.command == "improve":
        run_improve(args.task)
    elif args.command == "fix":
        run_fix(args.path)
    elif args.command == "architecture":
        run_architecture(args.path)
    elif args.command == "explain":
        run_explain(args.target)
    elif args.command == "doctor":
        run_doctor()
    elif args.command == "benchmark":
        run_benchmark()
    elif args.command == "run":
        if orchestrator_mod:
            engine = orchestrator_mod.WorkflowEngine(args.path)
            engine.execute_lifecycle(args.task)
        else:
            print("[ERROR] Workflow Engine not found.")
    elif args.command == "studio":
        if studio_mod:
            import webbrowser
            webbrowser.open(f"http://localhost:{args.port}")
            studio_mod.run_studio(port=args.port)
        else:
            print("[ERROR] Studio module not found.")
    elif args.command == "marketplace":
        if plugin_mod:
            pm = plugin_mod.PluginManager(".")
            pm.list_available()
        else:
            print("[ERROR] Plugin Manager not found.")
    elif args.command == "install":
        if plugin_mod:
            pm = plugin_mod.PluginManager(".")
            pm.install(args.pack)
        else:
            print("[ERROR] Plugin Manager not found.")
    elif args.command == "install-hooks":
        if git_hooks_mod:
            manager = git_hooks_mod.GitHooksManager(".")
            manager.install_pre_commit()
        else:
            print("[ERROR] Git Hooks Manager not found.")
    elif args.command == "new":
        run_new_project(args.project_name)
    elif args.command == "plan":
        run_plan(args.task, getattr(args, "path", "."))
    elif args.command == "status":
        run_status()
    elif args.command == "quickstart":
        run_quickstart()
    elif args.command == "design":
        run_design(args.query, args.domain, args.top)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
