import functools
import logging
import time
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, cast

from config.config import Config

F = TypeVar("F", bound=Callable[..., Any])


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Optional[Tuple[Type[Exception], ...]] = None,
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__module__)

            last_exception: Optional[Exception] = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if exceptions and not isinstance(e, exceptions):
                        raise

                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e.__class__.__name__}: {e}"
                        )
                        logger.warning(f"Retrying in {current_delay:.2f}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )

            if last_exception:
                raise last_exception

            return None

        return cast(F, wrapper)

    return decorator


def auto_log(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = logging.getLogger(func.__module__)

        func_name: str = func.__name__
        class_name: str = ""

        if args and hasattr(args[0], "__class__"):
            class_name = f"{args[0].__class__.__name__}."

        full_name: str = f"{class_name}{func_name}"
        step_name: str = full_name.replace("_", " ").title()

        logger.debug(f"[ENTER] {full_name}")
        start_time: float = time.time()

        def execute_with_logging() -> Any:
            try:
                result: Any = func(*args, **kwargs)
                duration: float = (time.time() - start_time) * 1000
                logger.debug(f"[EXIT] {full_name} - Duration: {duration:.2f}ms")
                return result
            except Exception as e:
                error_duration: float = (time.time() - start_time) * 1000
                logger.error(
                    f"[ERROR] {full_name} - Duration: {error_duration:.2f}ms - Error: {e}"
                )

                if Config.ALLURE_ENABLED:
                    try:
                        import allure

                        allure.attach(
                            str(e),
                            name=f"Error in {step_name}",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                    except ImportError:
                        logger.warning("Allure enabled but not installed")
                raise

        if Config.ALLURE_ENABLED:
            try:
                import allure

                with allure.step(step_name):
                    return execute_with_logging()
            except ImportError:
                logger.warning(
                    "Allure enabled but not installed - falling back to logging only"
                )
                return execute_with_logging()
        else:
            return execute_with_logging()

    return cast(F, wrapper)
