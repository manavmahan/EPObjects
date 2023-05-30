from idf_object import IDFObject
    
class PreprocessorMessage(IDFObject):
    __IDFName__ = 'Output:PreprocessorMessage'
    Properties = [
        'PreprocessorName',
        'ErrorSeverity',
        'MessageLine1',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
