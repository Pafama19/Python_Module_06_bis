
from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factories import CreatureFactory
from ex3.creature import Creature

from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    creatures: list[tuple[Creature, BattleStrategy]] = []

    for factory, strategy in opponents:
        creatures.append((factory.create_base(), strategy))

    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    try:
        for i in range(len(creatures)):
            for j in range(i + 1, len(creatures)):
                creature_one, strategy_one = creatures[i]
                creature_two, strategy_two = creatures[j]

                print("* Battle *")
                print(creature_one.describe())
                print("vs.")
                print(creature_two.describe())
                print("now fight!")

                strategy_one.act(creature_one)
                strategy_two.act(creature_two)

    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Shiftling+Aggressive) ]")
    battle([
        (flame_factory, normal),
        (transform_factory, aggressive),
    ])

    print()
    print("Tournament 1 (error)")
    print("[ (Shiftling+Aggressive), (Flameling+Aggressive) ]")
    battle([
        (transform_factory, aggressive),
        (flame_factory, aggressive),
    ])


if __name__ == "__main__":
    main()
