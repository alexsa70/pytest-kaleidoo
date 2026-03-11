from faker import Faker


class Fake:
    """Небольшая обертка над Faker для генерации тестовых значений."""

    def __init__(self, faker: Faker):
        self.faker = faker

    def word(self) -> str:
        return self.faker.word()

    def sentence(self) -> str:
        return self.faker.sentence()


fake = Fake(faker=Faker())
