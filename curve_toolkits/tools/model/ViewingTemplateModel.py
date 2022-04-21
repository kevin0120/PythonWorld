class ViewingTemplateModel:
    def __init__(self):
        self._bolt_number = None

    def set_bolt_number(self, bolt: str):
        self._bolt_number = bolt

    @property
    def bolt_number(self):
        return self._bolt_number
