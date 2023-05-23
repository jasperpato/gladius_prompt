import unittest
import datetime

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gladius_prompt import GladiusPrompt

# ----- dates -----

TODAY = datetime.date.today()

PAST_STRING = (TODAY - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
TODAY_STRING = TODAY.strftime("%Y-%m-%d")
FUTURE_STRING = (TODAY + datetime.timedelta(days=5)).strftime("%Y-%m-%d")

# ----- tests -----

class TestGladiusPrompt(unittest.TestCase):

    # ----- shop flight fares -----

    def _test_shop_commands(self, *args):
        g = GladiusPrompt(reply=False)
        for cmd, expected in args:
            g.onecmd(cmd)
            self.assertEqual(g.last_response, expected)

    def test_base_shop(self):
        self._test_shop_commands(
            [f'shop flight fares AAA AAB OneWay C {FUTURE_STRING}', 'OK'],
            [f'shop flight fares AAA AAB Return 5 C {FUTURE_STRING}', 'OK']
        )

    def test_shop_missing_args(self):
        self._test_shop_commands(
            [f'shop flight fares AAA AAB OneWay C', 'Error'],
            [f'shop flight fares AAA AAB Return 5 C', 'Error'],
        )

    def test_invalid_shop_airport(self):
        self._test_shop_commands(
            [f'shop flight fares AA AAB OneWay C {FUTURE_STRING}', 'Error'], # invalid origin
            [f'shop flight fares AAA AA OneWay C {FUTURE_STRING}', 'Error'], # invalid destination
        )

    def test_invalid_trip(self):
        self._test_shop_commands(
            [f'shop flight fares AAA AAB OneWay 10 C {FUTURE_STRING}', 'Error'], # trip length with OneWay
            [f'shop flight fares AAA AAB Return C {FUTURE_STRING}', 'Error'], # no trip length with Return
            [f'shop flight fares AAA AAB wrong C {FUTURE_STRING}', 'Error'], # wrong trip type with trip length
            [f'shop flight fares AAA AAB wrong 10 C {FUTURE_STRING}', 'Error'], # wrong trip type without trip length
            [f'shop flight fares AAA AAB Return 21 10 C {FUTURE_STRING}', 'Error'], # invalid trip length
        )

    def test_invalid_shop_cabin(self):
        self._test_shop_commands(
            [f'shop flight fares AAA AAB OneWay A {FUTURE_STRING}', 'Error'],
            [f'shop flight fares AAA AAB Return 5 20 {FUTURE_STRING}', 'Error'],
        )

    def test_invalid_shop_date(self):
        self._test_shop_commands(
            [f'shop flight fares AAA AAB OneWay C {PAST_STRING}', 'Error'], # before today
            [f'shop flight fares AAA AAB Return 5 20 {TODAY_STRING}', 'Error'], # today
        )

    # ----- air book req -----

    def _test_air_commands(self, *args):
        g = GladiusPrompt(reply=False)
        for cmds, expected in args:
            for cmd in cmds: g.onecmd(cmd)
            self.assertEqual(g.last_response, expected)

    def test_base_air(self):
        self._test_air_commands(
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'OK']
        )
        # multiple segments
        self._test_air_commands([
            ['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'OK']
        )

    def test_invalid_air_syntax(self):
        self._test_air_commands(
            [['wrong book req'], 'Error'],
            [['wrong book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5'], 'Error'],
            [['wrong book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],

            [['air book req', f'wrong AAA AAB AA1 {FUTURE_STRING} C 5'], 'Error'],
            [['air book req', f'wrong AAA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],

            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', 'wrong'], 'Error']
        )

    def test_invalid_air_airport(self):
        self._test_air_commands(
            [['air book req', f'seg AA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AA AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', f'seg AA AAB AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 5', f'seg AAA AA AA1 {FUTURE_STRING} C 5', 'EOC'], 'Error']
        )

    def test_invalid_flight(self):
        self._test_air_commands(
            [['air book req', f'seg AAA AAB AA {FUTURE_STRING} C 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB As1 {FUTURE_STRING} C 5', 'EOC'], 'Error'],
        )

    def test_invalid_air_date(self):
        self._test_air_commands(
            [['air book req', f'seg AAA AAB AA1 {PAST_STRING} C 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB AA1 {TODAY_STRING} C 5', 'EOC'], 'Error'],
        )

    def test_invalid_air_cabin(self):
        self._test_air_commands(
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} 0 5', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} G 5', 'EOC'], 'Error'],
        )

    def test_invalid_air_seat(self):
        self._test_air_commands(
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 0', 'EOC'], 'Error'],
            [['air book req', f'seg AAA AAB AA1 {FUTURE_STRING} C 11', 'EOC'], 'Error'],
        )

if __name__ == '__main__':
    unittest.main()