import re
import dns.resolver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class StrongPasswordValidator:
    regex = r"^(?=(?:.*[A-Z]){3,})(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>/?\[\]\\|`~]).{12,50}$"
    message = _(
        "Пароль должен содержать от 12 до 50 символов, минимум 3 заглавные буквы, "
        "хотя бы одну цифру и один спецсимвол."
    )

    def __call__(self, value: str):
        if not re.match(self.regex, value):
            raise ValidationError(self.message)


@deconstructible
class AllowedEmailValidator:
    """Валидатор для email с проверкой длины и допустимых доменов."""

    ALLOWED_EMAIL_DOMAINS = {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
        "icloud.com", "mail.com", "yandex.ru", "mail.ru", "rambler.ru",
        "bk.ru", "inbox.ru", "list.ru", "zoho.com", "protonmail.com",
        "tutanota.com", "gmx.com", "web.de", "yahoo.co.uk", "yahoo.co.in",
        "yahoo.fr", "yahoo.de", "qq.com", "naver.com", "daum.net", "hanmail.net",
        "rediffmail.com", "seznam.cz", "wp.pl", "o2.pl", "interia.pl",
        "t-online.de", "freenet.de", "gmx.net", "posteo.de"
    }
    MAX_LENGTH = 100

    def __call__(self, value: str):
        # Проверка длины email
        if len(value) > self.MAX_LENGTH:
            raise ValidationError(
                _("Длина email не должна превышать %(max_length)d символов."),
                params={"max_length": self.MAX_LENGTH},
            )
        
        # Проверка формата email
        match = re.match(r"^[\w\.-]+@([\w\.-]+)$", value)
        if not match:
            raise ValidationError(_("Некорректный формат email."))

        # Извлекаем домен из email
        domain = match.group(1).lower()

        # Проверка, что домен разрешён
        if domain not in self.ALLOWED_EMAIL_DOMAINS:
            raise ValidationError(
                _("Данный домен %(domain)s не разрешен."),
                params={"domain": domain},
            )

        # Проверка существования домена с помощью DNS
        try:
            dns.resolver.resolve(domain, 'MX')  # Проверка записи MX для домена
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            raise ValidationError(
                _("Домен %(domain)s не существует или не имеет MX записей."),
                params={"domain": domain},
            )

