from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Генерирует сообщение о выполненной тренировке для печати."""
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Не определён класс: ', self.__class__.__name__
            )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALL_1: int = 18
    COEFF_CALL_2: int = 20
    MINUTES: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALL_1 * self.get_mean_speed()
                - self.COEFF_CALL_2) * self.weight
                / self.M_IN_KM * (self.duration * self.MINUTES))

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALL_1: float = 0.035
    COEFF_CALL_2: float = 0.029
    COEFF_CALL_3: int = 2
    MINUTES: int = 60

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALL_1 * self.weight
                + (self.get_distance() ** self.COEFF_CALL_3
                 // self.height) * self.COEFF_CALL_2
                * self.weight) * self.duration * self.MINUTES)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALL_1: float = 1.1
    COEFF_CALL_2: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALL_1)
                * self.COEFF_CALL_2 * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_sport = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    type_treinung = dict_sport[workout_type]
    return type_treinung(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info_message = training.show_training_info()
    print(info_message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
