
from ex3.creature import Creature

from .battle_strategy import BattleStrategy
from .exceptions import InvalidStrategyError


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this normal strategy"
            )

        print(creature.attack())
