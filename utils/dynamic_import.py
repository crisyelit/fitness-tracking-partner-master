import importlib

class Dimport:

    @classmethod
    def get_class(cls, module_name, class_name):
        # __import__ method used
        # to fetch module

        module = importlib.import_module(module_name)

        # getting attribute by
        # getattr() method
        my_class = getattr(module, class_name)

        return my_class
