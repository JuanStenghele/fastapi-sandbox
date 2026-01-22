from system.conftest import Context


class TestHealthCheckController():
  def test_status(self, context: Context):
    response = context.client.get("/v1/health-check")
    assert response.status_code == 200
    data = response.json()
    assert data == {
      "api": "ok",
      "postgres_database": "ok"
    }
