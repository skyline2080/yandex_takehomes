import typing 
import functools 
import dataclasses 

# why this deco and custom ordering in general are required see comments in test() below

def ComparableWithSibling(tpl):
    if tpl.__name__ == "SessionStart":
        SiblingType = SessionClose
        IsInferiorToSibling = False
    elif tpl.__name__ == "SessionClose":
        SiblingType = SessionStart
        IsInferiorToSibling = True
    else:
        raise Exception("deco is meant to be used with SessionStart or SessionClose types only")

    def __lt__(self, other):
        if self.Time == other.Time:
            if isinstance(other, SiblingType):                    
                return IsInferiorToSibling
            
        return self.Time < other.Time

    def __eq__(self, other):
        if isinstance(other, self.__class__):                
            return self.Time == other.Time
            
        return False

    tpl.__lt__ = __lt__
    tpl.__eq__ = __eq__
    tpl = functools.total_ordering(tpl)

    return tpl


@ComparableWithSibling
class SessionStart(typing.NamedTuple):
    Time: int

    def register(self, session_rep):
        session_rep.RegisterStart(self.Time)


@ComparableWithSibling
class SessionClose(typing.NamedTuple):
    Time: int
    
    def register(self, session_rep):
        session_rep.RegisterClose()


@dataclasses.dataclass
class SessionRep:
    SessionMaxCount: int = 0
    SessionMaxCountTime: int = 0
    SessionCurrentCount: int = 0
    
    def RegisterStart(self, sessionstart_time):
        self.SessionCurrentCount += 1
        if self.SessionCurrentCount > self.SessionMaxCount:
            self.SessionMaxCount = self.SessionCurrentCount
            self.SessionMaxCountTime = sessionstart_time

    def RegisterClose(self):
        self.SessionCurrentCount -= 1

def test():
    s = ((1,3),(2,3),(2,4),(1,2),(2,5),(3,5),(1,3))
    
    def gen():
        for a, b in s:
            yield SessionStart(a)
            yield SessionClose(b)
    
    # it is imperative that 
    # SessionStart(2), SessionClose(2), SessionStart(2) be sorted in that order
    # SessionClose(2), SessionStart(2), SessionStart(2)
    # otherwise we risk reporting max count for a certain period 
    # before SessionClose for the same period is considered
    # hence custom ordering implemented above for both tuple types

    ls = list(gen())

    print("initial")
    for event in ls:
        print(event)


    ls = sorted(ls)

    print("sorted")
    for event in ls:
        print(event)


    rep = SessionRep()

    for session_event in ls:
        session_event.register(rep)
    
    print(f"max session count of {rep.SessionMaxCount} registered at {rep.SessionMaxCountTime}")