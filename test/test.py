import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        PROP = {
            'Catnip': 'Catnip',
            'FireCatnip': 'FireCatnip'
        }
        print(PROP['Catnip'])
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
