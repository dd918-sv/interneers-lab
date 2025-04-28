import unittest

def run_unit_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(['product.tests.test_category', 'product.tests.test_product'])
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

def run_integration_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('product.tests.test_integration')
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

if __name__ == '__main__':
    print("Running unit tests...")
    unit_results = run_unit_tests()
    
    print("\nRunning integration tests...")
    integration_results = run_integration_tests()
    
    if unit_results.wasSuccessful() and integration_results.wasSuccessful():
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed.")