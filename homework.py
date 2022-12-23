class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    # Возвращает строку сообщения с информацией о тренировке.
    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    # Расстояние, преодалеваемое за один шаг.
    LEN_STEP = 0.65
    # Константа для перевода метров в километры.
    M_IN_KM = 1000
    # Константа для перевода часов в минуты.
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type='Training'
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = training_type
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения (км/ч)."""
        speed: float = self.distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # У каждого вида тренировки свой подсчет.
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Возвращает объект класса сообщения.
        training_info: InfoMessage = InfoMessage(self.training_type,
                                                 self.duration,
                                                 self.distance,
                                                 self.speed,
                                                 self.calories)
        return training_info


class Running(Training):
    """Тренировка: бег."""
    # Константа для нормализации средний скорости.
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    # Константа для нормализации средний скорости.
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type='Running'
                 ) -> None:
        super().__init__(action, duration, weight, training_type)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.speed + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM
                           * (self.duration * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # Константа для нормализации веса.
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    # Константа для нормализации роста.
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    # Константа для перевода скорости из км/ч в м/с.
    KMH_IN_MSEC = 0.278
    # Константа для перевода роста из см в метры.
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height,
                 training_type='SportsWalking'
                 ) -> None:
        self.height = height / self.CM_IN_M
        super().__init__(action, duration, weight, training_type)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + ((self.speed * self.KMH_IN_MSEC)**2 / self.height)
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                           * self.weight) * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    # Расстояние, преодалеваемое за один гребок.
    LEN_STEP = 1.38
    # Константа для нормализации средней скорости.
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    # Константа для нормализации средней скорости.
    CALORIES_MEAN_SPEED_SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool,
                 training_type='Swimming'
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight, training_type)
        self.speed = self.get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.speed + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                           * self.CALORIES_MEAN_SPEED_SHIFT
                           * self.weight * self.duration)
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes: dict = {'SWM': Swimming,
                              'RUN': Running,
                              'WLK': SportsWalking}
    training: Training = training_classes[workout_type](*data)
    return training


def main(training: Training) -> str:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    result: str = info.get_message()
    print(result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
