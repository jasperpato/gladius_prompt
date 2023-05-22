import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gladius_prompt import GladiusPrompt

class TestGladiusPrompt(unittest.TestCase):
    def test_base_shop(self):
        g = GladiusPrompt(reply=False)

        g.onecmd('shop flight fares AAA AAB OneWay C 2023-06-01')
        self.assertEqual(g.last_response, 'OK')

        g.onecmd('shop flight fares AAA AAB Return 5 C 2023-06-01')
        self.assertEqual(g.last_response, 'OK')

    def test_base_air(self):
        g = GladiusPrompt(reply=False)
        g.onecmd('air book req')
        g.onecmd('seg AAA AAB AA1 2023-06-01 C 5')
        g.onecmd('EOC')
        self.assertEqual(g.last_response, 'OK')

if __name__ == '__main__':
    unittest.main()