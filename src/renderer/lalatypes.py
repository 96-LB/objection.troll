from types import EllipsisType, GenericAlias, UnionType
from typing import Any, Callable, ParamSpec, Protocol, Tuple, Type, TypeGuard, TypeVar, cast, get_args, get_origin, runtime_checkable

T = TypeVar('T')
T2 = TypeVar('T2')
P = ParamSpec('P')
P2 = ParamSpec('P2')
F = Callable
E = EllipsisType

jdict = dict[str, T]
AnyF = F[..., Any]
NullF = F[[], None]

@runtime_checkable
class Dictable(Protocol):
    def to_dict(self) -> dict[str, Any]:
        ...

ApiReturnValue = Dictable | jdict[Any] | list[Any] | Tuple[()]
ApiResponseValue = ApiReturnValue | Tuple[ApiReturnValue, int] | Tuple[ApiReturnValue, int, str]


def typecheck(obj: Any, cls: Type[T] | UnionType | GenericAlias) -> TypeGuard[T]:
    
    if cls is Any:
        return True
    
    if isinstance(cls, UnionType):
        return any(typecheck(obj, x) for x in get_args(cls))
    
    if isinstance(cls, GenericAlias):
        origin = get_origin(cls)
        args = get_args(cls)
        
        if origin is list and isinstance(obj, list):
            arg = args[0]
            for val in cast(list[Any], obj):
                if not typecheck(val, arg):
                    return False
            return True
        
        if origin is dict and isinstance(obj, dict):
            karg = args[0] if origin is dict else str
            varg = args[1] if origin is dict else args[0]
            for key, val in cast(dict[Any, Any], obj.items()):
                if not typecheck(key, karg):
                    return False
                if not typecheck(val, varg):
                    return False
            return True
        
        return False # don't care
    
    if isinstance(cls, type):
        return isinstance(obj, cls)
    
    return False


def typename(cls: Type[Any] | UnionType | GenericAlias) -> str:
    
    if isinstance(cls, UnionType):
        args = get_args(cls)
        
        # Optional[T] => T?
        if len(args) == 2 and type(None) in args:
            other = args[0] if args[1] is type(None) else args[1]
            return f'{typename(other)}?'
        
        return ' | '.join(typename(x) for x in get_args(cls))
    
    if isinstance(cls, GenericAlias):
        origin = get_origin(cls)
        args = get_args(cls)
        
        if origin is list:
            arg, = args
            return f'list[{typename(arg)}]'
        
        if origin is dict:
            karg, varg = args
            return f'dict[{typename(karg)}, {typename(varg)}]'
        
        return str(cls)
    
    if isinstance(cls, type):
        return cls.__name__
    
    return str(cls)
