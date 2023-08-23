

class ImproperlyConfigured(Exception):
    pass


class RequiredAttributeClass:
    """RequiredAttributeClass factors out generic code that checks defined attributes on classes."""

    required_attributes = []

    def __init__(self, *args, **kwargs):
        required_attributes = self.get_required_attributes()
        for attr in required_attributes:
            if getattr(self, attr) is None:
                raise NotImplementedError(attr)
        return super().__init__(*args, **kwargs)

    def get_required_attributes(self):
        return self.required_attributes