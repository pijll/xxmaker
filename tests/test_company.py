import unittest

from gamepart import Game
from gamepart import Company
import Colour


class TestCompany(unittest.TestCase):
    def test_standard_company(self):
        # Arrange

        # Act
        company = Company.Company("Some Railroad", abbreviation="SR", colour=Colour.red)

        # Assert
        self.assertEqual("Some Railroad", company.name, "Name")
        self.assertEqual(10, company.num_shares, "Number of shares")

    def test_add_to_game(self):
        # Arrange
        game = Game.Game("1801", "author", "credits")
        company = Company.Company("Some Railroad", abbreviation="SR", colour=Colour.red)

        # Act
        game.add_company(company)

        # Assert
        self.assertEqual(1, len(game.companies), "Number of companies")
        self.assertEqual("Some Railroad", game.companies["SR"].name)

