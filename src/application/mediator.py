from typing import Type, TypeVar, Dict, Any, Callable, Awaitable

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

class Mediator:
    def __init__(self):
        self._handlers: Dict[Type, Callable[[Any], Any]] = {}

    def register_handler(self, request_type: Type[TRequest], handler: Callable[[TRequest], TResponse]):
        self._handlers[request_type] = handler

    def send(self, request: Any) -> Any:
        handler = self._handlers.get(type(request))
        if not handler:
            raise ValueError(f"No handler registered for request type: {type(request)}")
        return handler(request)
