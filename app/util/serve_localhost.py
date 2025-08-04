import http.server
import socketserver
import threading
import webbrowser
import time
import os

class LocalHTTPServer:
    def __init__(self, port=8000, html_file="index.html"):
        self.port = port
        self.html_file = html_file
        self.server_thread = None
        self.httpd = None

    def handler_factory(self):
        parent = self
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=os.getcwd(), **kwargs)

            def do_GET(self):
                # Redirect root requests to the current html_file
                if self.path in ('/', '/index.html'):
                    self.path = f'/{parent.html_file}'
                return super().do_GET()
        return CustomHandler

    def open_browser(self):
        time.sleep(1)  # give server time to bind
        url = f"http://localhost:{self.port}/{self.html_file}"
        webbrowser.open(url, new=0, autoraise=True)

    def start_http_server(self):
        handler = self.handler_factory()
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            self.httpd = httpd
            print(f"Serving on http://localhost:{self.port} → {self.html_file}")
            httpd.serve_forever()

    def start(self):
        if not self.server_thread or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(
                target=self.start_http_server, daemon=True
            )
            self.server_thread.start()
            # open browser once on first start
            threading.Thread(target=self.open_browser).start()
        else:
            # already running, just open browser to the current file
            threading.Thread(target=self.open_browser).start()

    def change_html_file(self, new_file: str, open_browser: bool = True):
        """
        Switches to a different HTML file on the fly.
        If the server is running, the next request to "/" will serve the new file.
        """
        self.html_file = new_file
        print(f"Switched to serve: {new_file}")

        if open_browser and self.server_thread and self.server_thread.is_alive():
            # navigate your browser to the new page
            threading.Thread(target=self.open_browser).start()
        elif not self.server_thread or not self.server_thread.is_alive():
            # server isn’t running yet, so start it
            self.start()