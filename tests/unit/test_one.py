from unittest.mock import MagicMock, patch

def test_patch_vs_instance():
    session = MagicMock()
    print(type(session.merge))  # <class 'unittest.mock.MagicMock'>

    # patch.object работает на уровне КЛАССА, а не экземпляра
    with patch.object(session, "merge", MagicMock()):
        print(type(session.merge))  # <class 'method'>

from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# случай с моками
mock_session = MagicMock()
print(type(mock_session.merge))  # MagicMock
with patch.object(mock_session, "merge", MagicMock()):
    print(type(mock_session.merge))  # MagicMock

# случай с реальной сессией
real_session = Session()
print(type(real_session.merge))  # method
with patch.object(real_session, "merge", MagicMock()):
    print(type(real_session.merge))  # method