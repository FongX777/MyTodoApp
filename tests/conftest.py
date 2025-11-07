"""
Global pytest configuration for all tests.
"""

import sys
import os

# Set testing flag before any imports
os.environ["TESTING"] = "1"

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
