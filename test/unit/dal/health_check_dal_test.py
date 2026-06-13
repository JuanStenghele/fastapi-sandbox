from unittest.mock import MagicMock
from sqlmodel import Session
from dal.health_check_dal import HealthCheckDAL
from logging import Logger


class TestHealthCheckDal():
  def test_health_check_success(self):
    session_mock = MagicMock(spec = Session)
    session_mock.exec.return_value = 'ok'
    logger_mock = MagicMock(spec = Logger)
    instance = HealthCheckDAL(logger_mock)
    assert instance.health_check(session_mock) == True

  def test_health_check_fail(self):
    session_mock = MagicMock(spec = Session)
    session_mock.exec.side_effect = Exception('error')
    logger_mock = MagicMock(spec = Logger)
    instance = HealthCheckDAL(logger_mock)
    assert instance.health_check(session_mock) == False
