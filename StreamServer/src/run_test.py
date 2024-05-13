import pytest
import os

def run_tests():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    tests_dir = os.path.join(current_dir, 'tests')
    pytest.main([tests_dir])

if __name__ == "__main__":
    run_tests()
