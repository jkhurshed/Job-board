from .title_description import TitleDescriptionModel


class BaseModel(TitleDescriptionModel):

    class Meta:
        abstract = True
