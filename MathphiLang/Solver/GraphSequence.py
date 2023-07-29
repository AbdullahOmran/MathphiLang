
from collections.abc import Iterable

class GraphSequence(list):

    def __init__(self)->None:
        super().__init__()

    def __setitem__(self,index,item)->None:
        super().__setitem__(index,item)

    def insert(self,index,item)->None:
        super().insert(index,item)
    
    def append(self, item)->None:
        super().append(item)
    
    def extend(self, __iterable: Iterable) -> None:
        super().extend(__iterable)