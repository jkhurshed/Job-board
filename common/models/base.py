from .title_description import TitleDescriptionModel
from .uuid import UUIDmodel


class BaseModel(UUIDmodel, TitleDescriptionModel):

    class Meta:
        abstract = True
