import pytest
from src.application.use_cases.create_user import CreateUserUseCase


@pytest.mark.unit
def test_create_user_use_case_success(
    pure_mock_user_repo,
    user
):
    use_case = CreateUserUseCase(
        user_repo=pure_mock_user_repo
        )
    use_case.execute(user=user)

    pure_mock_user_repo.get.assert_called_once()
    pure_mock_user_repo.save.assert_called_once()
    assert pure_mock_user_repo.save.call_count == 1

@pytest.mark.unit
def test_create_user_use_case_user_exists(
    pure_mock_user_repo,
    user
):
    pure_mock_user_repo.get.return_value = user
    use_case = CreateUserUseCase(
        user_repo=pure_mock_user_repo
        )
    use_case.execute(user=user)

    pure_mock_user_repo.get.assert_called_once()
    pure_mock_user_repo.save.assert_not_called()
