from django import forms


class QuillAdminWidget(forms.Textarea):
    """Quill-редактор поверх скрытой textarea; хранит чистый HTML."""

    class Media:
        css = {"all": ("admin/widgets/quill/quill.snow.css",
                       "admin/widgets/quill/quill_init.css",)}
        js = ("admin/widgets/quill/quill.js",
              "admin/widgets/quill/quill_init.js")

    def __init__(self, attrs=None):
        attrs = {"class": "quill-html", "style": "display:none;", **(attrs or {})}
        super().__init__(attrs)
