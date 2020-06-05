class BaseErrorInheretence(Exception):
    pass


class SpecialError(BaseErrorInheretence):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # More code here if needed


raise SpecialError('stuff and things', error='something happened')
