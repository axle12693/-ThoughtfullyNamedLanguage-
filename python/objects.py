import uuid

class Connection:

    def __init__(self, start, end, realtionship) -> None:
        self.from_: str = start
        self.to: str = end
        self.r = realtionship


class Token:

    def __init__(self, id: str, **kwargs) -> None:
        self.uuid = kwargs.get('uuid', None) if kwargs.get('uuid', None) != None else uuid.uuid4()
        self.id: str = id
        self.c: list[Connection] = []


class Tree:

    def __init__(self) -> None:
        self.all: set[Token] = []
        self.ids: list[str] = []
        self.currentslice = 0

        self.all.append(Token('0'))
        return None
        
    def update(self) -> None:
        self.current = self.all[self.currentslice]
        for i, t in enumerate(self.all):
            if t not in self.ids:
                self.ids.insert(i, t.id)
        return None

    def append(self, t: Token) -> None:
        self.update()
        self.all.append(t)

    def connect(self, start: str, end: str, rel: str) -> None:
        self.update()
        s = Token(start)
        e = Token(end)
        for i in self.all:
            if i.id == s.id:
                s = i
            elif i.id == e.id:
                e = i
        
        s.c.insert(len(s.c), Connection(start, end, rel))
                

    def list(self) -> list[Connection]:
        self.update()
        return self.current

    def next(self, slice: int) -> None:
        self.update()
        self.currentslice = self.all.index(self.current.to.c[slice])
        return None
    
    def home(self) -> None:
        self.update()
        self.currentslice = 0
        return None