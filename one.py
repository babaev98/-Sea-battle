import random as rn


class MyException(Exception):
    pass


# Корабль
class Ship:
    def __init__(self, length, coordinates, directorion):
        self.length = length
        self.coordinates = coordinates
        self.directorion = directorion
        self.health_points = self.length

    def dots(self):
        if self.length == 1:
            return [self.coordinates]
        x = self.coordinates.x
        y = self.coordinates.y
        result = []
        result.append(self.coordinates)
        for n in range(1, self.length):
            if self.directorion == 'up':
                x -= 1
            elif self.directorion == 'down':
                x += 1
            elif self.directorion == 'left':
                y -= 1
            elif self.directorion == 'right':
                y += 1
            result.append(Dot(x, y))

        return result


# точка
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #убрать
        self.coordinates = [x, y]

    def __eq__(self, other):
        if not isinstance(other, (list, Dot)):
            raise TypeError('Не верные координаты')
        sc = other if isinstance(other, list) else other.coordinates
        return self.coordinates == sc


# поле
class Board:
    def __init__(self, hid:bool):
        self.field = [['O' for x in range(6)] for y in range(6)]
        self.list_ship = [3, 2, 2, 1, 1, 1, 1]
        self.ships = []
        self.hid = hid
        self.living_ships = 0

    # который ставит корабль на доску
    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot):
                raise MyException
            if self.field[dot.x][dot.y] != 'O':
                raise MyException
        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
        self.living_ships += 1
        self.ships.append(ship)
        self.contour(ship)

    # который обводит корабль по контуру
    def contour(self, ship):
        for dot in ship.dots():
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_dot = Dot(dot.x + x, dot.y + y)
                    if new_dot in ship.dots():
                        continue
                    if self.out(new_dot):
                        continue
                    self.field[new_dot.x][new_dot.y] = '-'

    def field_str(self):
        key = 0
        str_ = 'x 0 1 2 3 4 5  -y\n'
        for i1 in self.field:
            y = i1.copy()
            str_ += str(key) + '|' + ' '.join(y) + '\n'
            key += 1
        return str_

    def print_field(self):
        if self.hid:
            print(self.field_str())
        else:
            str_ = self.field_str()
            for x in str_:
                if x == '■':
                    x = 'O'
                    print(f'{x}', end='')
                else:
                    print(x, end='')
    # Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False,
    # если не выходит.
    @staticmethod
    def out(dot):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    # Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку,
    # нужно выбрасывать исключения).
    def shot(self, coordinates):
        if self.out(coordinates):
            raise MyException
        if self.field[coordinates.x][coordinates.y] in ('-', 'X'):
            raise MyException
        if self.field[coordinates.x][coordinates.y] == 'O':
            print('Промах')
            self.field[coordinates.x][coordinates.y] = '-'
            return False
        if self.field[coordinates.x][coordinates.y] == '■':
            for ship in self.ships:
                if coordinates in ship.dots():
                    self.field[coordinates.x][coordinates.y] = 'X'
                    ship.health_points -= 1
                    if ship.health_points == 0:
                        print('Убил')
                        self.ships.remove(ship)
                        self.living_ships -= 1
                    else:
                        print('Подбит')
                    return True


class Player:
    # move — метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске
    # (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся повторить ход. Метод должен возвращать True,
    # если этому игроку нужен повторный ход (например, если он выстрелом подбил корабль)
    def __init__(self, onw: Board, enemy: Board):
        self.onw = onw
        self.enemy = enemy

    def move(self):
        try:
            repeat_shot = self.ask()
        except MyException:
            self.move()
        else:
            self.enemy.print_field()
            if repeat_shot:
                self.move()

    def ask(self):
        pass


class AI(Player):

    def ask(self):
        x, y = rn.choice([i for i in range(6)]), rn.choice([i for i in range(6)])
        dot = Dot(x, y)
        return self.enemy.shot(dot)


class User(Player):

    def ask(self):
        coordinates_input = map(int, input('Координаты для выстрела -->').split())
        coordinates = Dot(*coordinates_input)
        return self.enemy.shot(coordinates)


class Game:

    def creating_a_field(self, result: Board) -> None:
        if result.hid:
            print(result.print_field())
            for length in result.list_ship:
                while True:
                    try:
                        self.creating_a_field_user(result, length)
                    except MyException:
                        print(' Недопустимое расположение  ')
                    except TypeError:
                        print(' Недопустимое расположение  ')
                    else:
                        break
                result.print_field()
            for x in range(6):
                for y in range(6):
                    if result.field[x][y] == '-':
                        result.field[x][y] = 'O'
            result.print_field()
        if not result.hid:
            print('AI строит свое поле')
            for length in result.list_ship:
                x = 0
                while True:
                    x += 1
                    try:
                        self.creating_a_field_ai(result, length)
                    except MyException:
                        pass
                    else:
                        break
                    if x > 1000:
                        result.living_ships = 0
                        result.field = [['O' for x in range(6)] for y in range(6)]
                        self.creating_a_field(result)
                        print('Не получилось сейчас попробует еще раз')
                        break

            for x in range(6):
                for y in range(6):
                    if result.field[x][y] == '-':
                        result.field[x][y] = 'O'
            print('Поле AI построено')

    def creating_a_field_user(self, result, length):
        coordinates = Dot(*map(int, input(f'Координаты куда разместить корабль с {length} палубами -->').split()))
        if length != 1:
            directorion = input('Введите напровления коробля (up, down, right, left) -->')
            if not (directorion in ['up', 'down', 'right', 'left']):
                raise MyException
        else:
            directorion = 'up'
        result.add_ship(Ship(length, coordinates, directorion))

    def creating_a_field_ai(self, result, length):
        x = rn.choice([x for x in range(6)])
        y = rn.choice([y for y in range(6)])
        coordinates = Dot(x, y)
        directorion = rn.choice(['up', 'down', 'right', 'left'])
        result.add_ship(Ship(length, coordinates, directorion))

    def __init__(self):
        self.user = User(Board(True), Board(False))
        self.field_user = self.user.onw
        self.ai = AI(self.user.enemy, self.user.onw)
        self.field_ai = self.ai.onw

    def greet(self):
        print('Привет. Эта игра в морской бой. Только тут поле не 10х10 а 6х6. Из доступных короблей 1 - трехпалубный\n'
              '2 - двухпалубных и 4 - однопалубных. Разместите их на своем поле учитывая их граници и растояние между\n'
              ' короблями, которое должно быть в одну клетку. Игра будет против компьютера и первый стреляющий будет \n'
              'определен рандомным способом. На поле существуют обозначения (0) - клетка коробля, (Х) - клетка \n'
              'подбитого коробля или убитого, (-) - клетка промоха. Кординаты для стрельбы указывать целыми числами \n'
              'не выходящими за пределы поля ( от 0 до 6) через пробел')

    def loop(self):
        first_move = rn.choice(['user', 'ai'])
        if first_move == 'user':
            print('Первый ход твой')
            one, two = self.user, self.ai
        else:
            print('Первый ход AI')
            one, two = self.ai, self.user
        while True:
            while one.move():
                pass
            if two.onw.living_ships == 0:
                print('Победил игрок')
                break
            while two.move():
                pass
            if one.onw.living_ships == 0:
                print('Игрок проиграл')
                break

    def start(self):
        self.greet()
        self.creating_a_field(self.user.onw)
        self.creating_a_field(self.ai.onw)
        self.loop()


while True:
    asd = Game()
    asd.start()
    x = int(input('Хотите продолжить. Если да то введите 1 а если нет то 0'))
    if not x:
        break
