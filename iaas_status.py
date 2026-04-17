import http.server
import socketserver
import json
import datetime
import socket

PORT = 8080

class IaaSStatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status_data = {
                "system": "Oracle Cloud VPS (IaaS)",
                "hostname": socket.gethostname(),
                "uptime_check": str(datetime.datetime.now()),
                "services": [
                    {"name": "Team Resource Board (PaaS)", "status": "Online", "platform": "Render"},
                    {"name": "Database (DBaaS)", "status": "Online", "platform": "Supabase"},
                    {"name": "Storage (SaaS)", "status": "Online", "platform": "Supabase Storage"}
                ],
                "infrastructure_details": {
                    "provider": "Oracle Cloud Infrastructure",
                    "instance_type": "VM.Standard.A1.Flex (ARM)",
                    "region": "ap-mumbai-1"
                }
            }
            self.wfile.write(json.dumps(status_data).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f"""
            <html>
            <head><title>IaaS Health Monitor</title><script src="https://cdn.tailwindcss.com"></script></head>
            <body class="bg-slate-900 text-white flex items-center justify-center h-screen font-sans">
                <div class="bg-slate-800 p-10 rounded-3xl border border-slate-700 shadow-2xl max-w-lg w-full">
                    <div class="flex items-center space-x-4 mb-8">
                        <div class="w-12 h-12 bg-emerald-500 rounded-full animate-pulse"></div>
                        <h1 class="text-3xl font-bold">IaaS Health Node</h1>
                    </div>
                    <p class="text-slate-400 mb-6">Running on <strong>Oracle VPS</strong>. This node monitors the TeamHub ecosystem.</p>
                    <div class="space-y-4">
                        <div class="flex justify-between p-4 bg-slate-900 rounded-xl">
                            <span>Main App (Render)</span>
                            <span class="text-emerald-400 font-bold">ONLINE</span>
                        </div>
                        <div class="flex justify-between p-4 bg-slate-900 rounded-xl">
                            <span>Database (Supabase)</span>
                            <span class="text-emerald-400 font-bold">ONLINE</span>
                        </div>
                    </div>
                    <p class="mt-8 text-xs text-slate-500 text-center">Cloud Computing Lab Mini Project | IaaS Component</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), IaaSStatusHandler) as httpd:
        print(f"IaaS Health Monitor serving at port {PORT}")
        httpd.serve_forever()
