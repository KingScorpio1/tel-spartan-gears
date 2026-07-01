import http.server
import json
import os
from datetime import datetime

class CSVHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
        csv_content = body.get('csv', '')
        auto = body.get('auto', False)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if auto:
            filename = 'trebuchet_training_autosave.csv'
            filepath = os.path.join(base_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'filename': filename, 'auto': True}).encode())
        elif self.path == '/save-csv':
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'trebuchet_training_{ts}.csv'
            filepath = os.path.join(base_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'filename': filename}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 8765
    server = http.server.HTTPServer(('', port), CSVHandler)
    print(f'Serving at http://localhost:{port}')
    server.serve_forever()
