# Foobartory by Thibaut Cavalié

# Le but est de coder une chaîne de production automatique de `foobar`.
#
# On dispose au départ de 2 robots, qui sont chacun capables d'effectuer
# plusieurs actions :
#
# -   Se déplacer pour changer d'activité : occupe le robot pendant 5 secondes.
# -   Miner du `foo` : occupe le robot pendant 1 seconde.
# -   Miner du `bar` : occupe le robot pendant un temps aléatoire compris
#     entre 0.5 et 2 secondes.
# -   Assembler un `foobar` à partir d'un `foo` et d'un `bar` :
#     occupe le robot pendant 2 secondes.
#     L'opération a 60% de chances de succès ; en cas d'échec le `bar`
#     peut être réutilisé, le `foo` est perdu.
#
# Tu as de grands entrepôts, la gestion des stocks n'est pas un problème.
# En revanche, la législation impose la traçabilité des pièces ayant servi à
# fabriquer les `foobars` :
# chaque `foo` et chaque `bar` doivent avoir un numéro de série unique qu'on
# doit retrouver sur le `foobar` en sortie d'usine
#
# On souhaite ensuite accélérer la production pour prendre rapidement le
# contrôle du marché des `foobar`. Les robots peuvent effectuer
# de nouvelles actions:
#
# -   Vendre des `foobar` : 10s pour vendre de 1 à 5 foobar, on gagne 1€
#     par foobar vendu
# -   Acheter un nouveau robot pour 3€ et 6 `foo`, 0s
#
# Le jeu s'arrête quand on a 30 robots.
#
# Note:
# 1 seconde du jeu n'a pas besoin d'être une seconde réelle.
# Le choix des actvités n'a _pas besoin d'être optimal_
# (pas besoin de faire des maths), seulement fonctionnel.


import asyncio
import logging
import random
import sys
import uuid

# logging configuration to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Foo:
    uid = (
        uuid.uuid4()
    )  # no "id" because it's a built-in function, no "uuid" because imported

    def __str__(self):
        return f"Foo id #{self.uid}"


class Bar:
    uid = uuid.uuid4()

    def __str__(self):
        return f"Bar id #{self.uid}"


class Factory:
    second_multiplier = 1 / 100
    foo_list = []
    bar_list = []
    foo_bar_list = []
    euros = 0
    robot_number = 0


class Robot:
    number: str
    Factory: Factory

    def __init__(self, factory):
        self.factory = factory
        self.factory.robot_number += 1
        self.number = self.factory.robot_number
        logger.info(f"robot #{self.number} created")

    async def move(self):
        await asyncio.sleep(5 * self.factory.second_multiplier)

    async def build_foo(self):
        await asyncio.sleep(1 * self.factory.second_multiplier)
        foo = Foo()
        self.factory.foo_list.append(foo)
        logger.info(
            f"robot #{self.number} created {foo}, "
            f"{len(self.factory.foo_list)} foos now"
        )

    async def build_bar(self):
        random_sleep_time = max(0.5, random.random() * 2)
        await asyncio.sleep(random_sleep_time * self.factory.second_multiplier)
        bar = Bar()
        self.factory.bar_list.append(bar)
        logger.info(
            f"robot #{self.number} created {bar}, "
            f"{len(self.factory.bar_list)} bars now"
        )

    async def assemble_foo_bar(self):
        await asyncio.sleep(2 * self.factory.second_multiplier)
        # take foo and bar from the lists
        try:
            foo = self.factory.foo_list.pop(0)
        except IndexError:
            logger.warning(f"robot #{self.number} failed to assemble, no foo available")
            return
        try:
            bar = self.factory.bar_list.pop(0)
        except IndexError:
            logger.warning(f"robot #{self.number} failed to assemble, no bar available")
            return
        # 60% of success
        if random.random() > 0.6:
            logger.warning(
                f"robot #{self.number} failed to assemble, "
                f"{foo} is lost, {bar} is reused"
            )
            self.factory.bar_list.append(bar)
            return
        # let's assemble
        self.factory.foo_bar_list.append((foo, bar))
        logger.info(
            f"robot #{self.number} succeeded to assemble {foo} and {bar}, "
            f"{len(self.factory.foo_bar_list)} foobars now"
        )

    async def sell_foobars(self):
        # Is there enough foobars to be sold ?
        if len(self.factory.foo_bar_list) == 0:
            logger.warning(f"0 foobars, robot #{self.number} can not sell")
            return
        # sell a maximum of 5 foobars
        for _ in range(5):
            try:
                (foo, bar) = self.factory.foo_bar_list.pop(0)
            except IndexError:
                pass
            else:
                self.factory.euros += 1
                logger.info(
                    f"robot #{self.number} sold {foo} and {bar}, "
                    f"we have {self.factory.euros} euros now"
                )

    async def buy_new_robot(self):
        # Is there 3 euros and 6 foos ?
        if self.factory.euros < 3 or len(self.factory.foo_list) < 6:
            logger.warning(
                f"not enough euros and foos, "
                f"robot #{self.number} can not create new robot"
            )
            return
        self.factory.foo_list = self.factory.foo_list[6:]
        self.factory.euros -= 3
        robot = Robot(self.factory)
        logger.info(f"robot #{self.number} created new robot #{robot.number}")
        loop = asyncio.get_event_loop()
        if self.factory.robot_number == 30:
            logger.info("SUCCESS! 30 robots created!")
            # exit cleanly
            loop.stop()
        loop.create_task(robot.start())

    async def start(self):
        await self.move()
        # make random activity
        func = random.choice(
            [
                self.build_foo,
                self.build_bar,
                self.assemble_foo_bar,
                self.sell_foobars,
                self.buy_new_robot,
            ]
        )
        await func()
        # start again
        await self.start()


def main():
    logger.info("Factory starts")
    factory = Factory()
    robot1 = Robot(factory)
    robot2 = Robot(factory)
    loop = asyncio.get_event_loop()
    loop.create_task(robot1.start())
    loop.create_task(robot2.start())
    loop.run_forever()


if __name__ == "__main__":
    main()
