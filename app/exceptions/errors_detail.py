from enum import Enum


class ProjectErrorDetail(str, Enum):
    """Описания ошибок"""

    PROJECT_NOT_FOUND = 'Проект не найден!'
    PROJECT_ALREADY_EXISTS = 'Проект с таким именем уже существует!'
    PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
    PROJECT_ALREADY_INVESTED = (
        'В проект были внесены средства, не подлежит удалению!'
    )
    PROJECT_AMOUNT_LESS_INVESTING = (
        'Нельзя установить значение full_amount меньше уже вложенной суммы.'
    )
    PROJECT_BLANK_NAME = 'Название проекта не может быть пустым!'
    PROJECT_BLANK_DESCRIPTION = 'Описание проекта не может быть пустым!'
