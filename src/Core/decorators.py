import functools
import logging
import time
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__module__)

            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )

            raise last_exception

        return wrapper

    return decorator


def auto_log(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)

        func_name = func.__name__
        class_name = ""

        if args and hasattr(args[0], "__class__"):
            class_name = f"{args[0].__class__.__name__}."

        full_name = f"{class_name}{func_name}"

        logger.debug(f"[ENTER] {full_name}")

        start_time = time.time()

        try:
            result = func(*args, **kwargs)

            duration = (time.time() - start_time) * 1000

            logger.debug(f"[EXIT] {full_name} - Duration: {duration:.2f}ms")

            return result

        except Exception as e:
            duration = (time.time() - start_time) * 1000

            logger.error(
                f"[ERROR] {full_name} - Duration: {duration:.2f}ms - Error: {e}"
            )
            raise

    return wrapper
