from typing import Optional

from app.exceptions.errors_detail import ProjectErrorDetail


class ProjectException(Exception):
    """Базовый класс исключений для проектов"""

    detail: Optional[str] = None

    def __init__(self, detail: Optional[str] = None) -> None:
        if detail is not None:
            self.detail = detail


class BlankProjectName(ProjectException, ValueError):
    """Пустое имя проекта"""

    detail = ProjectErrorDetail.PROJECT_BLANK_NAME


class BlankProjectDescription(ProjectException, ValueError):
    """Пустое описание проекта"""

    detail = ProjectErrorDetail.PROJECT_BLANK_DESCRIPTION