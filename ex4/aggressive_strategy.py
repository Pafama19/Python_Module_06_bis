
from ex3.creature import Creature
from ex3.transform_capability import TransformCapability

from .battle_strategy import BattleStrategy
from .exceptions import InvalidStrategyError


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )

        capability = creature
        if isinstance(capability, TransformCapability):
            print(capability.transform())
            print(creature.attack())
            print(capability.revert())
