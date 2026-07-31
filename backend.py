from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import os
import sqlite3

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8000'))
DB_PATH = os.environ.get('DB_PATH', 'maison_boutique.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


class BoutiqueHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', '0'))
        data = parse_qs(self.rfile.read(length).decode('utf-8'))

        if parsed.path == '/api/review':
            product = data.get('product', [''])[0].strip()
            rating = data.get('rating', ['0'])[0].strip()
            comment = data.get('comment', [''])[0].strip()
            if product and comment and rating:
                conn = self._db()
                conn.execute('INSERT INTO reviews (product, rating, comment) VALUES (?, ?, ?)', (product, int(rating), comment))
                conn.commit()
                conn.close()
                self._send_json(200, {'success': True, 'message': 'Review recorded successfully.'})
            else:
                self._send_json(400, {'success': False, 'message': 'Incomplete review data.'})
            return

        if parsed.path == '/api/order':
            item = data.get('item', [''])[0].strip()
            size = data.get('size', [''])[0].strip()
            color = data.get('color', [''])[0].strip()
            quantity = data.get('quantity', [''])[0].strip()
            phone = data.get('phone', [''])[0].strip()
            if item and size and color and quantity and phone:
                conn = self._db()
                conn.execute('INSERT INTO orders (item, size, color, quantity, phone) VALUES (?, ?, ?, ?, ?)', (item, size, color, quantity, phone))
                conn.commit()
                conn.close()
                self._send_json(200, {'success': True, 'message': 'Order received. A boutique representative will contact you shortly.'})
            else:
                self._send_json(400, {'success': False, 'message': 'Incomplete order data.'})
            return

        self._send_json(404, {'success': False, 'message': 'Not found'})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/reviews':
            conn = self._db()
            rows = conn.execute('SELECT product, rating, comment FROM reviews ORDER BY id DESC LIMIT 20').fetchall()
            conn.close()
            payload = [dict(row) for row in rows]
            self._send_json(200, payload)
            return

        if parsed.path == '/api/orders':
            conn = self._db()
            rows = conn.execute('SELECT item, size, color, quantity, phone FROM orders ORDER BY id DESC LIMIT 20').fetchall()
            conn.close()
            payload = [dict(row) for row in rows]
            self._send_json(200, payload)
            return

        if parsed.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('index.html', 'rb') as handle:
                self.wfile.write(handle.read())
            return
        if parsed.path.endswith(('.html', '.css', '.js', '.txt', '.xml', '.png', '.jpg', '.jpeg')):
            file_path = parsed.path.lstrip('/')
            try:
                with open(file_path, 'rb') as handle:
                    content = handle.read()
                self.send_response(200)
                if file_path.endswith('.css'):
                    self.send_header('Content-Type', 'text/css; charset=utf-8')
                elif file_path.endswith('.js'):
                    self.send_header('Content-Type', 'application/javascript; charset=utf-8')
                else:
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self._send_json(404, {'success': False, 'message': 'File not found'})
            return
        self._send_json(404, {'success': False, 'message': 'Not found'})


if __name__ == '__main__':
    init_db()
    server = HTTPServer((HOST, PORT), BoutiqueHandler)
    print(f'Serving Maison Boutique on http://{HOST}:{PORT}')
    server.serve_forever()
