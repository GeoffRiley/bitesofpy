class Car:
    """
    Car class
    """

    def __init__(self, model, color):
        self.model = model
        self.color = color

    def __eq__(self, other_car):
        return (
                self.model.lower() == other_car.model.lower()
                and self.color.lower() == other_car.color.lower()
        )

    @staticmethod
    def age(days):
        """if / elif / else for exercise sake, if there would
           be more conditions we would use a dict / mapping
        """
        if days == 7:
            return "A week old"
        elif days == 365:
            return "A year old"
        else:
            return "Neither a week, nor a year old"

    @staticmethod
    def has_same_configuration(config1, config2):
        if not isinstance(config1, list) or not isinstance(config2, list):
            raise TypeError()
        return config1 == config2


def is_same_car_color_and_model(car1, car2):
    """
    Returns true if car1 and car2 are the of same model and color
    """
    return car1 == car2


def is_same_instance_of_car(car1, car2):
    """
    Returns true if car1 and car2 are exactly the same object (instance)
    """
    return car1 is car2
