class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        print(f'Длительность: {"{:10.3f}".format(self.duration)} ч.;'
              f' Дистанция: {"{:10.3f}".format(self.distance)} км;'
              f' Ср. скорость: {"{:10.3f}".format(self.selfspeed)} км/ч;'
              f' Потрачено ккал: {"{:10.3f}".format(self.calories)}.')


class Training:
    """Базовый класс тренировки."""
    # Расстояние, преодалеваемое за один шаг.
    LEN_STEP = 0.65
    # Константа для перевода метров в километры.
    M_IN_KM = 1000
   
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duraction = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self, distance) -> float:
        """Получить среднюю скорость движения."""
        speed = distance / self.duraction
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # У каждого вида тренировки свой подсчет.
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Возвращает объект класса сообщения.
        training_info = InfoMessage()
        return training_info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.speed + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_K * (self.duration * 60))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.weight + (self.speed ** 2 / self.height)
                    * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                    * (self.duraction * 60))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.speed + self.CALORIES_MEAN_SPEED_MULTIPLIE)
                    * self.CALORIES_MEAN_SPEED_SHIFT
                    * self.weight * self.duraction)
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.get_distance)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking}

    char_class: Training = training_classes[workout_type]()
    return char_class.__init__(data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info
    str_info = info.get_message
    print(str_info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)