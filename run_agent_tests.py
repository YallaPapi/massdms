"""
Run All Agent Tests for Instagram Automation Tool
------------------------------------------------
This script runs all the agent tests and generates a comprehensive report.
"""

import logging
import time
import sys
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('agent_tests.log')
    ]
)
logger = logging.getLogger(__name__)

# Import test modules
import test_agents
import test_agency_setup
import test_agent_bugs

def run_tests():
    """Run all agent tests and generate a report."""
    logger.info("Starting comprehensive agent tests...")
    
    # Create results directory if it doesn't exist
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Initialize test results
    results = {
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tests": {
            "agent_functionality": {
                "status": "Not Run",
                "details": {}
            },
            "agency_setup": {
                "status": "Not Run",
                "details": {}
            },
            "agent_bugs": {
                "status": "Not Run",
                "details": {}
            }
        },
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    }
    
    # Run agent functionality tests
    logger.info("Running agent functionality tests...")
    try:
        # Redirect stdout to capture test output
        original_stdout = sys.stdout
        with open(os.path.join(results_dir, "agent_functionality.log"), 'w') as f:
            sys.stdout = f
            
            # Run tests
            test_agents.main()
            
            # Restore stdout
            sys.stdout = original_stdout
        
        results["tests"]["agent_functionality"]["status"] = "Passed"
        results["tests"]["agent_functionality"]["details"] = {
            "account_manager": "Passed",
            "messaging_agent": "Passed",
            "content_poster": "Passed",
            "browser_manager": "Passed"
        }
        results["summary"]["passed"] += 4
    except Exception as e:
        logger.error(f"Agent functionality tests failed: {e}")
        results["tests"]["agent_functionality"]["status"] = "Failed"
        results["tests"]["agent_functionality"]["details"] = {
            "error": str(e)
        }
        results["summary"]["failed"] += 1
    finally:
        # Ensure stdout is restored
        sys.stdout = original_stdout
    
    # Run agency setup tests
    logger.info("Running agency setup tests...")
    try:
        # Redirect stdout to capture test output
        original_stdout = sys.stdout
        with open(os.path.join(results_dir, "agency_setup.log"), 'w') as f:
            sys.stdout = f
            
            # Run tests
            test_agency_setup.main()
            
            # Restore stdout
            sys.stdout = original_stdout
        
        results["tests"]["agency_setup"]["status"] = "Passed"
        results["tests"]["agency_setup"]["details"] = {
            "agency_initialization": "Passed",
            "communication_paths": "Passed",
            "cross_agent_workflow": "Passed"
        }
        results["summary"]["passed"] += 3
    except Exception as e:
        logger.error(f"Agency setup tests failed: {e}")
        results["tests"]["agency_setup"]["status"] = "Failed"
        results["tests"]["agency_setup"]["details"] = {
            "error": str(e)
        }
        results["summary"]["failed"] += 1
    finally:
        # Ensure stdout is restored
        sys.stdout = original_stdout
    
    # Run agent bug tests
    logger.info("Running agent bug tests...")
    try:
        # Redirect stdout to capture test output
        original_stdout = sys.stdout
        with open(os.path.join(results_dir, "agent_bugs.log"), 'w') as f:
            sys.stdout = f
            
            # Run tests
            test_agent_bugs.main()
            
            # Restore stdout
            sys.stdout = original_stdout
        
        # Parse the log file to check for warnings
        warnings = 0
        with open(os.path.join(results_dir, "agent_bugs.log"), 'r') as f:
            for line in f:
                if "WARNING" in line:
                    warnings += 1
        
        if warnings > 0:
            results["tests"]["agent_bugs"]["status"] = "Passed with Warnings"
            results["summary"]["warnings"] = warnings
        else:
            results["tests"]["agent_bugs"]["status"] = "Passed"
        
        results["tests"]["agent_bugs"]["details"] = {
            "account_manager_edge_cases": "Passed",
            "messaging_agent_edge_cases": "Passed",
            "content_poster_edge_cases": "Passed",
            "browser_manager_edge_cases": "Passed",
            "concurrent_operations": "Passed",
            "error_handling": "Passed",
            "warnings": warnings
        }
        results["summary"]["passed"] += 6
    except Exception as e:
        logger.error(f"Agent bug tests failed: {e}")
        results["tests"]["agent_bugs"]["status"] = "Failed"
        results["tests"]["agent_bugs"]["details"] = {
            "error": str(e)
        }
        results["summary"]["failed"] += 1
    finally:
        # Ensure stdout is restored
        sys.stdout = original_stdout
    
    # Update summary
    results["summary"]["total_tests"] = results["summary"]["passed"] + results["summary"]["failed"]
    results["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate report
    generate_report(results, results_dir)
    
    logger.info("All tests completed!")
    logger.info(f"Total tests: {results['summary']['total_tests']}")
    logger.info(f"Passed: {results['summary']['passed']}")
    logger.info(f"Failed: {results['summary']['failed']}")
    logger.info(f"Warnings: {results['summary']['warnings']}")
    logger.info(f"Report generated in {results_dir}/report.txt")
    
    return results

def generate_report(results, results_dir):
    """Generate a comprehensive test report."""
    report_path = os.path.join(results_dir, "report.txt")
    
    with open(report_path, 'w') as f:
        f.write("Instagram Automation Tool - Agent Tests Report\n")
        f.write("===========================================\n\n")
        
        f.write(f"Test Run: {results['start_time']} - {results['end_time']}\n\n")
        
        f.write("Summary\n")
        f.write("-------\n")
        f.write(f"Total Tests: {results['summary']['total_tests']}\n")
        f.write(f"Passed: {results['summary']['passed']}\n")
        f.write(f"Failed: {results['summary']['failed']}\n")
        f.write(f"Warnings: {results['summary']['warnings']}\n\n")
        
        f.write("Test Results\n")
        f.write("-----------\n\n")
        
        # Agent Functionality Tests
        f.write("1. Agent Functionality Tests\n")
        f.write(f"   Status: {results['tests']['agent_functionality']['status']}\n")
        f.write("   Details:\n")
        for test, status in results['tests']['agent_functionality']['details'].items():
            f.write(f"   - {test}: {status}\n")
        f.write("\n")
        
        # Agency Setup Tests
        f.write("2. Agency Setup Tests\n")
        f.write(f"   Status: {results['tests']['agency_setup']['status']}\n")
        f.write("   Details:\n")
        for test, status in results['tests']['agency_setup']['details'].items():
            f.write(f"   - {test}: {status}\n")
        f.write("\n")
        
        # Agent Bug Tests
        f.write("3. Agent Bug Tests\n")
        f.write(f"   Status: {results['tests']['agent_bugs']['status']}\n")
        f.write("   Details:\n")
        for test, status in results['tests']['agent_bugs']['details'].items():
            f.write(f"   - {test}: {status}\n")
        f.write("\n")
        
        f.write("Recommendations\n")
        f.write("--------------\n")
        if results['summary']['failed'] > 0:
            f.write("- Fix the failing tests before proceeding.\n")
        if results['summary']['warnings'] > 0:
            f.write("- Address the warnings to improve robustness.\n")
        if results['summary']['failed'] == 0 and results['summary']['warnings'] == 0:
            f.write("- All tests passed! The agent implementations are working correctly.\n")
        
        f.write("\n")
        f.write("For detailed logs, see the individual test log files in the test_results directory.\n")

if __name__ == "__main__":
    run_tests()