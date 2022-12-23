class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return str(message)


class Training:
    """Базовый класс тренировки."""
    # Расстояние, преодалеваемое за один шаг.
    LEN_STEP = 0.65
    # Константа для перевода метров в километры.
    M_IN_KM = 1000
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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения (км/ч)."""
        speed = self.distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # У каждого вида тренировки свой подсчет.
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Возвращает объект класса сообщения.
        training_info: InfoMessage = InfoMessage(self.training_type,
                                                 self.duration, self.distance,
                                                 self.speed, self.calories)
        return training_info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
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
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.speed + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
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
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + ((self.speed * self.KMH_IN_MSEC)**2 / self.height)
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight) * (self.duration * self.MIN_IN_H))
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
                 count_pool,
                 training_type='Swimming'
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight, training_type)
        self.speed = self.get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.speed + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                    * self.CALORIES_MEAN_SPEED_SHIFT
                    * self.weight * self.duration)
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking}

    training: Training = training_classes[workout_type](*data)
    return training


def main(training: Training) -> str:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    result = info.get_message()
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
