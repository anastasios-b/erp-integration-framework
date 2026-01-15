#!/usr/bin/env python3
"""
Test runner for ERP to Eshop integration framework
Provides a simple way to run all tests with detailed output
"""

import sys
import os
import unittest
import time
from io import StringIO

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_tests():
    """Run all tests and return results"""
    print("=" * 70)
    print("ERP to Eshop Integration Framework - Test Runner")
    print("=" * 70)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = '.'  # Current directory (tests/)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create a test runner with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    # Run tests and capture results
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Get the output
    output = stream.getvalue()
    print(output)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Overall result
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {len(result.failures) + len(result.errors)} test(s) failed!")
        return 1

def run_specific_test(test_name):
    """Run a specific test module or class"""
    print(f"Running specific test: {test_name}")
    
    try:
        suite = unittest.TestLoader().loadTestsFromName(test_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error loading test '{test_name}': {e}")
        return 1

def main():
    """Main entry point for test runner"""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        return run_specific_test(test_name)
    else:
        # Run all tests
        return run_tests()

if __name__ == '__main__':
    sys.exit(main())
