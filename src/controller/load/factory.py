from abc import ABC, abstractmethod
from typing import Any, Optional, Union, Iterable

class IFactory(ABC):
    _subclasses_instances={}
    def __init__(self) -> None:
        super().__init__()
        IFactory._subclasses_instances[self.__class__.__name__]=self
    
    @abstractmethod
    def create(self, name:Optional[str]=None, **kwargs)->Any:
        raise NotImplementedError

    @classmethod
    def init_subclasses(cls)->None:
        [c() for c in cls.__subclasses__() if not c.__name__ in cls._subclasses_instances]

    @classmethod
    def factory(cls, factory_name, default=None)->Union['IFactory',None]:
        return cls._subclasses_instances.get(factory_name, default)

    @classmethod
    def instanciate(cls, data:Iterable[object])->Iterable[Any]:
        PNAME='factory'
        cls.init_subclasses()
        for i in data:
            if hasattr(i, PNAME):
                factory:IFactory=cls.factory(getattr(i, PNAME))
            elif PNAME in i:
                factory:IFactory=cls.factory(i[PNAME])
            if factory:
                yield factory.create(**i)