from common.models import BaseModel


class Category(BaseModel):
    
    """
    Category model
    fields:
        - id (uuid)
        - title
        - description
    """

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
