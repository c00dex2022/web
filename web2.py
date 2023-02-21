import http.server
import socketserver
import logging
import base64
import csv

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        logging.info('%s - - [%s] "%s" %s %s',
                     self.client_address[0],
                     self.log_date_time_string(),
                     self.requestline,
                     code,
                     size)

    def do_POST(self):
        # Get the length of the request data
        content_length = int(self.headers['Content-Length'])
        
        # Read the request data
        request_data = self.rfile.read(content_length).decode('utf-8')
        
        # Find the 'i=' parameter in the request
        i_param_index = request_data.find("i=")
        
        if i_param_index != -1:
            # Find the end of the request line
            http_index = request_data.find("HTTP/1.1", i_param_index)
            
            if http_index != -1:
                # Get the base64-encoded data between the 'i=' parameter and the end of the request line
                data = request_data[i_param_index + 2 : http_index].strip()
                
                # Decode the base64-encoded data
                decoded_data = base64.b64decode(data).decode('utf-8')
                
                # Write the decoded data to a CSV file
                with open('output.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([decoded_data])

        # Send a response to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Success')

Handler = RequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

print(f"Serving at port {PORT}")
httpd.serve_forever()
