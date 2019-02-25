
import pytest
import asynctest

from . import example


# There you could define this as separate functions/organize in different ways,
# just keeping it all together here for the example.
@pytest.fixture()
def patch_do_something(monkeypatch):
    """Fixture that mocks out the 'do_something' coroutine."""
    def mocker():
        return 'xyz'

    mock = asynctest.CoroutineMock(
        example.do_something,
        side_effect=mocker,
    )
    monkeypatch.setattr(example, 'do_something', mock)
    return patch_do_something


@pytest.mark.asyncio
async def test_build_string_ok():
    """Test that we get back some expected result."""
    res = await example.build_string()
    assert res == 'foo bar'


@pytest.mark.asyncio
@pytest.mark.usefixtures('patch_do_something')
async def test_build_string_error():
    """Test getting back unexpected data and failing. This will require some
    coroutine mocking.
    """
    with pytest.raises(ValueError):
        await example.build_string()
