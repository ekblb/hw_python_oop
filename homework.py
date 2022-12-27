from dataclasses import dataclass, asdict
from typing import List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    # Расстояние, преодалеваемое за один шаг.
    LEN_STEP: float = 0.65
    # Константа для перевода метров в километры.
    M_IN_KM: int = 1000
    # Константа для перевода часов в минуты.
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения (км/ч)."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод расчета калорий'
                                  ' должен быть определен в дочернем классе')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    # Константа для нормализации средний скорости.
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    # Константа для нормализации средний скорости.
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # Константа для нормализации веса.
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    # Константа для нормализации роста.
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    # Константа для перевода скорости из км/ч в м/с.
    KMH_IN_MSEC: float = 0.278
    # Константа для перевода роста из см в метры.
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        self.height = height / self.CM_IN_M
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((speed * self.KMH_IN_MSEC)**2 / self.height)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    # Расстояние, преодалеваемое за один гребок.
    LEN_STEP: float = 1.38
    # Константа для нормализации средней скорости.
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    # Константа для нормализации средней скорости.
    CALORIES_MEAN_SPEED_SHIFT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        return ((speed + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes: dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    try:
        return training_classes[workout_type](*data)
    except KeyError:
        raise KeyError('Неопределенный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
