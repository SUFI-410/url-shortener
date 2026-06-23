from django.db import models


class ShortURL(models.Model):

    original_url = models.URLField()

    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True
    )

    click_count = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
