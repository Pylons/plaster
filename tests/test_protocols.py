def test_wsgi_protocol():
    from plaster.protocols import IWSGIProtocol

    class WSGILoader(IWSGIProtocol):  # pragma: no cover
        def get_wsgi_app(self, name=None, defaults=None):
            def app(environ, start_response):
                start_response(b"200 OK", [(b"Content-Type", b"text/plain")])
                return [b"hello world"]

            return app

        def get_wsgi_app_settings(self, name=None, defaults=None):
            settings = defaults.copy() if defaults else {}
            return settings

        def get_wsgi_filter(self, name=None, defaults=None):
            def filter(app):
                def wrapper(environ, start_response):
                    return app(environ, start_response)

                return wrapper

            return filter

        def get_wsgi_server(self, name=None, defaults=None):
            def server(app):
                from wsgiref.simple_server import make_server

                server = make_server("0.0.0.0", 8080, app)
                server.serve_forever()

    WSGILoader()
