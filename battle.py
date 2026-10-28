
from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factories import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing factory")
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(
    factory_one: CreatureFactory,
    factory_two: CreatureFactory,
) -> None:
    creature_one = factory_one.create_base()
    creature_two = factory_two.create_base()

    print("Testing battle")
    print(creature_one.describe())
    print("vs.")
    print(creature_two.describe())
    print("fight!")
    print(creature_one.attack())
    print(creature_two.attack())


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    test_factory(flame_factory)
    test_factory(transform_factory)
    test_battle(flame_factory, transform_factory)


if __name__ == "__main__":
    main()
