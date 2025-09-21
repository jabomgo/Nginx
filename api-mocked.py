import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class MockHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))

        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        server = self.server
        id_val = getattr(server, "mock_id", None)
        domain_val = getattr(server, "mock_domain", None)

        if id_val is None or domain_val is None:
            self._send_json({"error": "server not configured"}, status=500)
            return

        data = {
            "id": id_val,
            "domain": domain_val,
            "message": f"olá da api {id_val}, dominio {domain_val}"
        }
        self._send_json(data)
    def do_POST(self):
        return self.do_GET()

def parse_args():
    p = argparse.ArgumentParser(description="Mock API que retorna id, domain e mensagem.")
    p.add_argument("--id", required=True, help="ID que a API deve retornar")
    p.add_argument("--domain", required=True, help="Domínio que a API deve retornar")
    p.add_argument("--host", default="127.0.0.1", help="Host para bind (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=8000, help="Porta (default: 8000)")
    return p.parse_args()

def run_server(mock_id, mock_domain, host="127.0.0.1", port=8000):
    server = HTTPServer((host, port), MockHandler)
    server.mock_id = mock_id
    server.mock_domain = mock_domain
    print(f"Mock API rodando em http://{host}:{port}/")
    print(f"Retornando -> id: {mock_id}, domain: {mock_domain}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Encerrando.")
        server.server_close()

if __name__ == "__main__":
    args = parse_args()
    run_server(args.id, args.domain, host=args.host, port=args.port)
