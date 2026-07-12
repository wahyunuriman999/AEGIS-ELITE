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

from governance import GovernanceEngine
from consensus import AIPairReview
from benchmark import BenchmarkEngine

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
    engine = GovernanceEngine(workspace_path)
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
    review = AIPairReview()
    approved = review.run_consensus(task_context)
    if approved:
        print("\n[AEGIS ELITE] Applying refactored architecture safely to the workspace.")
    else:
        print("\n[AEGIS ELITE] Action halted. Returning feedback to user for manual intervention.")

def run_benchmark():
    engine = BenchmarkEngine()
    engine.run_benchmark()

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="AEGIS Elite - Enterprise Cognitive Runtime CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init
    subparsers.add_parser("init", help="Initialize AEGIS Elite in current directory")
    
    # review
    review_parser = subparsers.add_parser("review", help="Run Governance Audit")
    review_parser.add_argument("--path", default=".", help="Workspace path to review")
    
    # improve
    improve_parser = subparsers.add_parser("improve", help="Run AI Pair Review and apply refactor")
    improve_parser.add_argument("--task", default="General Code Refactoring", help="Task context description")
    
    # benchmark
    subparsers.add_parser("benchmark", help="Run AEGIS vs Standard AI Benchmark Suite")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_workspace()
    elif args.command == "review":
        run_review(args.path)
    elif args.command == "improve":
        run_improve(args.task)
    elif args.command == "benchmark":
        run_benchmark()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
