from middlewares.cors_middleware import build_cors_middleware


class TestCORSMiddleware():
  def test_cors_middleware_disabled(self):
    assert build_cors_middleware(cors_middleware_enabled = False, origins = ["http://localhost:5173"]) is None

  def test_cors_middleware_enabled(self):
    assert build_cors_middleware(cors_middleware_enabled = True, origins = ["http://localhost:5173"]) is not None
