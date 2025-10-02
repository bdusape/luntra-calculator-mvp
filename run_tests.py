#!/usr/bin/env python3
"""
Test runner script for LUNTRA Calculator MVP
Provides convenient commands for running different test suites
"""

import sys
import subprocess
import argparse

def run_pytest_command(args):
    """Run pytest with the provided arguments"""
    cmd = ["pytest"] + args
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="LUNTRA Calculator Test Runner")
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--formulas', action='store_true', help='Run formula tests only')
    parser.add_argument('--house-hack', action='store_true', help='Run house-hack specific tests')
    parser.add_argument('--whole-unit', action='store_true', help='Run whole-unit specific tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--fast', action='store_true', help='Run tests with minimal output')
    parser.add_argument('--verbose', action='store_true', help='Run tests with verbose output')
    
    args = parser.parse_args()
    
    # Base pytest arguments
    pytest_args = []
    
    if args.verbose:
        pytest_args.extend(['-v', '--tb=long'])
    elif args.fast:
        pytest_args.extend(['-q', '--tb=no'])
    
    if args.coverage:
        pytest_args.extend(['--cov=calculator', '--cov=app', '--cov-report=term-missing'])
    
    # Test selection
    if args.unit:
        pytest_args.extend(['-m', 'unit'])
    elif args.integration:
        pytest_args.extend(['-m', 'integration'])
    elif args.formulas:
        pytest_args.extend(['-m', 'formulas'])
    elif args.house_hack:
        pytest_args.extend(['-m', 'house_hack'])
    elif args.whole_unit:
        pytest_args.extend(['-m', 'whole_unit'])
    elif not args.all:
        # Default: run all tests if no specific category selected
        pass
    
    # Run the tests
    result = run_pytest_command(pytest_args)
    return result.returncode

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)