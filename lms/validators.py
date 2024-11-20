from rest_framework.serializers import ValidationError


class YouTubeValidator:
    """Проверка ссылок на сторонние ресурсы, кроме youtube.com"""

    def __init__(
        self, field
    ):  # field - данные с которыми будут сравниваться входящие данные от пользователя
        self.field = field

    def __call__(self, value):  # value - те данные которые приходят от пользователя
        video_url = dict(value).get(self.field)
        # если в передаваемых данных value есть значение "youtube.com" с ключом "video_url", то:
        if bool(dict(value).get("video_url")) and not bool("youtube.com" in video_url):
            raise ValidationError("Недопустимая ссылка")
