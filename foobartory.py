# Foobartory by Thibaut Cavalié

# Le but est de coder une chaîne de production automatique de `foobar`.
#
# On dispose au départ de 2 robots, qui sont chacun capables d'effectuer plusieurs actions :
#
# -   Se déplacer pour changer d'activité : occupe le robot pendant 5 secondes.
# -   Miner du `foo` : occupe le robot pendant 1 seconde.
# -   Miner du `bar` : occupe le robot pendant un temps aléatoire compris entre 0.5 et 2 secondes.
# -   Assembler un `foobar` à partir d'un `foo` et d'un `bar` : occupe le robot pendant 2 secondes.
#     L'opération a 60% de chances de succès ; en cas d'échec le `bar` peut être réutilisé, le `foo` est perdu.
#
# Tu as de grands entrepôts, la gestion des stocks n'est pas un problème.
# En revanche, la législation impose la traçabilité des pièces ayant servi à fabriquer les `foobars` :
# chaque `foo` et chaque `bar` doivent avoir un numéro de série unique qu'on doit retrouver sur le `foobar` en sortie d'usine
#
# On souhaite ensuite accélérer la production pour prendre rapidement le contrôle du marché des `foobar`. Les robots peuvent effectuer de nouvelles actions:
#
# -   Vendre des `foobar` : 10s pour vendre de 1 à 5 foobar, on gagne 1€ par foobar vendu
# -   Acheter un nouveau robot pour 3€ et 6 `foo`, 0s
#
# Le jeu s'arrête quand on a 30 robots.
#
# Note:
# 1 seconde du jeu n'a pas besoin d'être une seconde réelle.
# Le choix des actvités n'a _pas besoin d'être optimal_ (pas besoin de faire des maths), seulement fonctionnel.


import asyncio
import logging
import sys
import random
import uuid

# logging configuration to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SECOND_MULTIPLIER = 1/100
FOO_LIST = []
BAR_LIST = []
FOO_BAR_LIST = []
MY_EUROS = 0
ROBOT_NUMBER = 0


class Foo():
    uid = uuid.uuid4()  # no "id" because it's a built-in function, no "uuid" because it's imported

    def __str__(self):
        return f'Foo id #{self.uid}'


class Bar():
    uid = uuid.uuid4()

    def __str__(self):
        return f'Bar id #{self.uid}'


class Robot():
    number: str

    def __init__(self):
        global ROBOT_NUMBER
        ROBOT_NUMBER += 1
        self.number = ROBOT_NUMBER
        logger.info(f'robot #{self.number} created')
        if ROBOT_NUMBER == 30:
            logger.info(f'SUCCESS! 30 robots created!')
            sys.exit()

    async def move(self):
        logger.debug(f'robot #{self.number} moving')
        await asyncio.sleep(5 * SECOND_MULTIPLIER)

    async def build_foo(self):
        await asyncio.sleep(1 * SECOND_MULTIPLIER)
        foo = Foo()
        FOO_LIST.append(foo)
        logger.info(f'robot #{self.number} created {foo}, {len(FOO_LIST)} foos now')

    async def build_bar(self):
        random_sleep_time = max(0.5, random.random() * 2)
        await asyncio.sleep(random_sleep_time * SECOND_MULTIPLIER)
        bar = Bar()
        BAR_LIST.append(bar)
        logger.info(f'robot #{self.number} created {bar}, {len(BAR_LIST)} bars now')

    async def assemble_foo_bar(self):
        logger.debug(f'robot #{self.number} trying to assemble foo and bar')
        await asyncio.sleep(2 * SECOND_MULTIPLIER)
        # take foo and bar from the lists
        try:
            foo = FOO_LIST.pop(0)
        except IndexError:
            logger.warning(f'robot #{self.number} failed to assemble, no foo available')
            return
        try:
            bar = FOO_LIST.pop(0)
        except IndexError:
            logger.warning(f'robot #{self.number} failed to assemble, no bar available')
            return
        # 60% of success
        if random.random() > 0.6:
            logger.warning(f'robot #{self.number} failed to assemble, {foo} is lost, {bar} is reused')
            BAR_LIST.append(bar)
            return
        # let's assemble
        FOO_BAR_LIST.append((foo, bar))
        logger.info(f'robot #{self.number} succeeded to assemble {foo} and {bar}, {len(FOO_BAR_LIST)} foobars now')

    async def sell_foobars(self):
        # Is there enough foobars to be sold ?
        if len(FOO_BAR_LIST) == 0:
            logger.warning(f'0 foobars, can not sell')
            return
        # sell a maximum of 5 foobars
        for _ in range(5):
            try:
                (foo, bar) = FOO_BAR_LIST.pop(0)
                global MY_EUROS
                MY_EUROS += 1
                logger.info(f'{foo} and {bar} sold, we have {MY_EUROS} euros now')
            except IndexError:
                pass

    async def buy_new_robot(self):
        # Is there 3 euros and 6 foos ?
        global MY_EUROS
        global FOO_LIST
        if MY_EUROS < 3 or len(FOO_LIST) < 6:
            logger.warning('not enough euros and foos, can not create new robot')
            return
        FOO_LIST = FOO_LIST[6:]
        MY_EUROS -= 3
        robot = Robot()
        loop = asyncio.get_event_loop()
        loop.create_task(robot.start())

    async def start(self):
        await self.move()
        # make random activity
        func = random.choice([
            self.build_foo,
            self.build_bar,
            self.assemble_foo_bar,
            self.sell_foobars,
            self.buy_new_robot
        ])
        await func()
        # start again
        await self.start()


def main():
    logger.info('Factory starts')
    robot1 = Robot()
    robot2 = Robot()
    loop = asyncio.get_event_loop()
    loop.create_task(robot1.start())
    loop.create_task(robot2.start())
    loop.run_forever()


if __name__ == "__main__":
    main()
