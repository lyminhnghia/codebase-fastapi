import pytest
import asyncio
from app.cores.prepare_file import async_wrap


def test_async_wrap():
    # Test function to be wrapped
    def test_func(x, y):
        return x + y

    # Wrap the function
    async_test_func = async_wrap(test_func)

    # Test the wrapped function
    @pytest.mark.asyncio
    async def test_wrapped_function():
        result = await async_test_func(1, 2)
        assert result == 3

    # Run the test
    asyncio.run(test_wrapped_function())
