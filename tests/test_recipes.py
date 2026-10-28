"""Validate the complete recipe set without requiring Minecraft or Gradle."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT / 'src/main/resources/data/toolmerge/recipes'


class RecipeTests(unittest.TestCase):
    def test_exact_upgrade_recipes(self):
        expected = {}
        for source, target in [('wooden', 'stone'), ('stone', 'iron'),
                               ('iron', 'diamond'), ('diamond', 'netherite')]:
            for tool in ('sword', 'pickaxe', 'axe'):
                name = f'{source}_{tool}_to_{target}_{tool}'
                expected[name] = {
                    'type': 'minecraft:crafting_shapeless',
                    'ingredients': [{'item': f'minecraft:{source}_{tool}'}] * 2,
                    'result': {'item': f'minecraft:{target}_{tool}', 'count': 1},
                }
        actual = {p.stem: json.loads(p.read_text()) for p in RECIPES.glob('*.json')}
        self.assertEqual(actual, expected)

    def test_no_netherite_ingredients_or_mixed_tools(self):
        for path in RECIPES.glob('*.json'):
            with self.subTest(recipe=path.name):
                data = json.loads(path.read_text())
                ingredients = data['ingredients']
                self.assertEqual(len(ingredients), 2)
                self.assertEqual(ingredients[0], ingredients[1])
                self.assertNotIn('netherite', ingredients[0]['item'])

    def test_resource_pack_format(self):
        pack = json.loads((ROOT / 'src/main/resources/pack.mcmeta').read_text())
        self.assertEqual(pack['pack']['pack_format'], 6)


if __name__ == '__main__':
    unittest.main()
