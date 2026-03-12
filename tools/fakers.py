from faker import Faker


class Fake:
    """Небольшая обертка над Faker для генерации тестовых значений."""

    def __init__(self, faker: Faker):
        self.faker = faker

    def word(self) -> str:
        return self.faker.word()

    def sentence(self) -> str:
        return self.faker.sentence()

    def fake_email(self) -> str:
        return self.faker.email()

    def fake_org_name(self) -> str:
        return f"{self.faker.word()}-{self.faker.word()}".lower().replace(" ", "-")

    def fake_domain(self) -> str:
        return self.faker.domain_name()

    def fake_username(self) -> str:
        return self.faker.user_name()

    def fake_first_name(self) -> str:
        return self.faker.first_name()

    def fake_last_name(self) -> str:
        return self.faker.last_name()

    def fake_password(self, length: int = 12) -> str:
        return self.faker.password(length=length)


fake = Fake(faker=Faker())


def fake_email() -> str:
    return fake.fake_email()


def fake_org_name() -> str:
    return fake.fake_org_name()


def fake_domain() -> str:
    return fake.fake_domain()


def fake_username() -> str:
    return fake.fake_username()


def fake_first_name() -> str:
    return fake.fake_first_name()


def fake_last_name() -> str:
    return fake.fake_last_name()


def fake_password(length: int = 12) -> str:
    return fake.fake_password(length=length)
