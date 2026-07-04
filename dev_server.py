"""Локальный dev-сервер без кеширования — чтобы правки были видны сразу, без Ctrl+Shift+R."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_head(self):
        # Отключаем ответы 304 (If-Modified-Since), чтобы всегда отдавать свежий файл.
        if "If-Modified-Since" in self.headers:
            del self.headers["If-Modified-Since"]
        if "If-None-Match" in self.headers:
            del self.headers["If-None-Match"]
        return super().send_head()


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), NoCacheHandler).serve_forever()
