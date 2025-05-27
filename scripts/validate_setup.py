#!/usr/bin/env python3
"""
Script to validate the complete setup of TransparenciaBR-Analytics project.
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class SetupValidator:
    """Validate project setup and dependencies."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            }
        }
    
    def check(self, name: str, condition: bool, message: str = "", 
              warning: bool = False) -> bool:
        """Record a check result."""
        status = "passed" if condition else ("warning" if warning else "failed")
        
        self.results["checks"][name] = {
            "status": status,
            "message": message or f"{name} {'passed' if condition else 'failed'}"
        }
        
        self.results["summary"]["total"] += 1
        if condition:
            self.results["summary"]["passed"] += 1
        elif warning:
            self.results["summary"]["warnings"] += 1
        else:
            self.results["summary"]["failed"] += 1
        
        # Print result
        symbol = "✓" if condition else ("⚠" if warning else "✗")
        color = "\033[92m" if condition else ("\033[93m" if warning else "\033[91m")
        reset = "\033[0m"
        
        print(f"{color}{symbol}{reset} {name}: {message}")
        
        return condition
    
    def check_python_version(self) -> bool:
        """Check Python version."""
        version = sys.version_info
        is_valid = version >= (3, 8)
        
        return self.check(
            "Python Version",
            is_valid,
            f"Python {version.major}.{version.minor}.{version.micro} "
            f"({'OK' if is_valid else 'Requires >= 3.8'})"
        )
    
    def check_environment_variables(self) -> bool:
        """Check required environment variables."""
        required_vars = [
            "TRANSPARENCIA_API_TOKEN",
            "TRANSPARENCIA_API_EMAIL"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        all_present = len(missing_vars) == 0
        
        # Check .env file exists
        env_file = self.project_root / ".env"
        self.check(
            ".env file",
            env_file.exists(),
            f"{'Found' if env_file.exists() else 'Not found'}"
        )
        
        return self.check(
            "Environment Variables",
            all_present,
            f"All required variables set" if all_present 
            else f"Missing: {', '.join(missing_vars)}"
        )
    
    def check_dependencies(self) -> bool:
        """Check Python dependencies."""
        required_packages = [
            "requests",
            "python-dotenv",
            "pandas",
            "numpy",
            "pytest",
            "streamlit",
            "plotly",
            "notebook"
        ]
        
        missing_packages = []
        installed_packages = []
        
        for package in required_packages:
            try:
                importlib.import_module(package.replace("-", "_"))
                installed_packages.append(package)
            except ImportError:
                missing_packages.append(package)
        
        all_installed = len(missing_packages) == 0
        
        self.check(
            "Python Dependencies",
            all_installed,
            f"{len(installed_packages)}/{len(required_packages)} packages installed" +
            (f" (Missing: {', '.join(missing_packages)})" if missing_packages else "")
        )
        
        return all_installed
    
    def check_directory_structure(self) -> bool:
        """Check project directory structure."""
        required_dirs = [
            "src",
            "src/api",
            "src/data",
            "src/utils",
            "src/models",
            "src/dashboard",
            "data",
            "data/raw",
            "data/processed",
            "data/cache",
            "notebooks",
            "notebooks/01_exploratory",
            "notebooks/02_analysis",
            "tests",
            "scripts",
            "docs",
            "logs",
            "reports",
            "models"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
        
        all_exist = len(missing_dirs) == 0
        
        self.check(
            "Directory Structure",
            all_exist,
            f"All required directories exist" if all_exist 
            else f"Missing: {', '.join(missing_dirs[:3])}{'...' if len(missing_dirs) > 3 else ''}"
        )
        
        # Create missing directories
        if missing_dirs:
            for dir_path in missing_dirs:
                (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)
            print(f"  → Created {len(missing_dirs)} missing directories")
        
        return all_exist
    
    def check_api_connection(self) -> bool:
        """Test API connection."""
        try:
            from src.api.client import TransparenciaAPIClient
            
            client = TransparenciaAPIClient()
            connected = client.test_connection()
            
            return self.check(
                "API Connection",
                connected,
                "Successfully connected to Portal da Transparência API" if connected
                else "Failed to connect to API"
            )
        except Exception as e:
            return self.check(
                "API Connection",
                False,
                f"Error: {str(e)}"
            )
    
    def check_git_repository(self) -> bool:
        """Check Git repository status."""
        try:
            # Check if it's a git repository
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            is_git_repo = result.returncode == 0
            
            if is_git_repo:
                # Get current branch
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                branch = result.stdout.strip()
                
                # Check for uncommitted changes
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                has_changes = bool(result.stdout.strip())
                
                message = f"On branch '{branch}'"
                if has_changes:
                    message += " (uncommitted changes)"
                
                return self.check(
                    "Git Repository",
                    is_git_repo,
                    message,
                    warning=has_changes
                )
            else:
                return self.check(
                    "Git Repository",
                    False,
                    "Not a Git repository"
                )
        except FileNotFoundError:
            return self.check(
                "Git Repository",
                False,
                "Git not installed"
            )
    
    def check_cache_directory(self) -> bool:
        """Check cache directory and permissions."""
        cache_dir = self.project_root / "data" / "cache"
        
        exists = cache_dir.exists()
        is_writable = os.access(cache_dir, os.W_OK) if exists else False
        
        # Count cached files
        cache_count = len(list(cache_dir.glob("*.json"))) if exists else 0
        
        return self.check(
            "Cache Directory",
            exists and is_writable,
            f"{'Writable' if is_writable else 'Not writable'}" +
            f" ({cache_count} cached items)" if exists else "Not found"
        )
    
    def run_tests(self) -> bool:
        """Run basic tests."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            success = result.returncode == 0
            
            # Parse test output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if " passed" in line or " failed" in line:
                    self.check(
                        "Test Suite",
                        success,
                        line.strip()
                    )
                    break
            else:
                self.check(
                    "Test Suite",
                    success,
                    "Tests completed" if success else "Tests failed"
                )
            
            return success
        except Exception as e:
            return self.check(
                "Test Suite",
                False,
                f"Error running tests: {str(e)}"
            )
    
    def check_notebooks(self) -> bool:
        """Check if notebooks exist."""
        notebook_dir = self.project_root / "notebooks"
        notebooks = list(notebook_dir.glob("**/*.ipynb"))
        
        has_notebooks = len(notebooks) > 0
        
        return self.check(
            "Jupyter Notebooks",
            has_notebooks,
            f"Found {len(notebooks)} notebooks" if has_notebooks
            else "No notebooks found",
            warning=not has_notebooks
        )
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = []
        report.append("\n" + "="*60)
        report.append("SETUP VALIDATION REPORT")
        report.append("="*60)
        report.append(f"Timestamp: {self.results['timestamp']}")
        report.append(f"Project: TransparenciaBR-Analytics")
        report.append("")
        
        # Summary
        summary = self.results['summary']
        report.append("SUMMARY:")
        report.append(f"  Total checks: {summary['total']}")
        report.append(f"  ✓ Passed: {summary['passed']}")
        report.append(f"  ⚠ Warnings: {summary['warnings']}")
        report.append(f"  ✗ Failed: {summary['failed']}")
        report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS:")
        for check_name, result in self.results['checks'].items():
            symbol = {
                "passed": "✓",
                "warning": "⚠",
                "failed": "✗"
            }[result['status']]
            
            report.append(f"  {symbol} {check_name}: {result['message']}")
        
        # Recommendations
        if summary['failed'] > 0 or summary['warnings'] > 0:
            report.append("")
            report.append("RECOMMENDATIONS:")
            
            if "Environment Variables" in self.results['checks'] and \
               self.results['checks']["Environment Variables"]['status'] == "failed":
                report.append("  1. Set up environment variables:")
                report.append("     - Copy .env.template to .env")
                report.append("     - Fill in your API credentials")
            
            if "Python Dependencies" in self.results['checks'] and \
               self.results['checks']["Python Dependencies"]['status'] == "failed":
                report.append("  2. Install missing dependencies:")
                report.append("     pip install -r requirements.txt")
            
            if "Git Repository" in self.results['checks'] and \
               self.results['checks']["Git Repository"]['status'] == "failed":
                report.append("  3. Initialize Git repository:")
                report.append("     git init")
                report.append("     git add .")
                report.append("     git commit -m 'Initial commit'")
        
        report.append("")
        report.append("="*60)
        
        return "\n".join(report)
    
    def save_report(self, report: str) -> None:
        """Save report to file."""
        reports_dir = self.project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"setup_validation_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nReport saved to: {report_file}")
    
    def run_validation(self) -> bool:
        """Run all validation checks."""
        print("\n🔍 Running Setup Validation...\n")
        
        # Run all checks
        self.check_python_version()
        self.check_environment_variables()
        self.check_dependencies()
        self.check_directory_structure()
        self.check_api_connection()
        self.check_git_repository()
        self.check_cache_directory()
        self.check_notebooks()
        
        # Optionally run tests (can be slow)
        if "--skip-tests" not in sys.argv:
            self.run_tests()
        else:
            print("⚠ Test Suite: Skipped (use --skip-tests to run)")
        
        # Generate and save report
        report = self.generate_report()
        print(report)
        self.save_report(report)
        
        # Return overall success
        return self.results['summary']['failed'] == 0


def main():
    """Main entry point."""
    validator = SetupValidator()
    success = validator.run_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()