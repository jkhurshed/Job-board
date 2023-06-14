from .title_description import TitleDescriptionModel
from .uuid import UUIDmodel


class BaseModel(UUIDmodel, TitleDescriptionModel):
    """
    Abstact Base model with uuid pk and create and update time
    """

    class Meta:
        abstract = True
