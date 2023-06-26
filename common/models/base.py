from .title_description import TitleDescriptionModel


class BaseModel(TitleDescriptionModel):
    """
    Abstact Base model with uuid pk and create and update time
    """

    class Meta:
        abstract = True
