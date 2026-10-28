
from ex3 import TransformCreatureFactory
from ex3.transform_capability import TransformCapability
from ex3.creature import Creature


def test_transformation(creature: Creature) -> None:
    if not isinstance(creature, TransformCapability):
        return

    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


def main() -> None:
    factory = TransformCreatureFactory()

    print("Testing Creature with transform capability")

    print("base:")
    base = factory.create_base()
    test_transformation(base)

    print("evolved:")
    evolved = factory.create_evolved()
    test_transformation(evolved)


if __name__ == "__main__":
    main()
