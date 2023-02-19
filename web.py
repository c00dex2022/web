import http.server
import socketserver
import logging

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        logging.info('%s - - [%s] "%s" %s %s',
                     self.client_address[0],
                     self.log_date_time_string(),
                     self.requestline,
                     code,
                     size)

Handler = RequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

print(f"Serving at port {PORT}")
httpd.serve_forever()
