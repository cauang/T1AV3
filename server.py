import http.server
import socketserver
import json
import os
import sys

root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from src.uf import UnionFind
from src.graph import EdgeWeightedGraph, Edge

PORT = 8000

def solve_mst(points, grid_w=20, grid_h=20):
    N = len(points)
    if N <= 0:
        return {
            "grid_owners": [],
            "grid_distances": [],
            "candidate_edges": [],
            "mst_weight": 0
        }
        
    uf = UnionFind(N)
    coords_to_idx = {}
    unique_points = []
    
    for i in range(N):
        x, y = points[i]
        if (x, y) in coords_to_idx:
            orig_idx = coords_to_idx[(x, y)]
            uf.union(orig_idx, i)
        else:
            coords_to_idx[(x, y)] = i
            unique_points.append((x, y, i))
            
    grid_cells = grid_w * grid_h
    owner = [-1] * grid_cells
    dist = [999999] * grid_cells
    
    q = []
    for x, y, idx in unique_points:
        cell = x * grid_h + y
        owner[cell] = idx
        dist[cell] = 0
        q.append((x, y))
        
    head = 0
    seen_edges = set()
    grafo = EdgeWeightedGraph(N)
    
    add_edge = grafo.add_edge
    abs_func = abs
    
    while head < len(q):
        x, y = q[head]
        head += 1
        
        curr_cell = x * grid_h + y
        curr_owner = owner[curr_cell]
        curr_dist = dist[curr_cell]
        
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < grid_w and 0 <= ny < grid_h:
                n_cell = nx * grid_h + ny
                n_owner = owner[n_cell]
                
                if n_owner == -1:
                    owner[n_cell] = curr_owner
                    dist[n_cell] = curr_dist + 1
                    q.append((nx, ny))
                elif n_owner != curr_owner:
                    u, v = curr_owner, n_owner
                    if u > v:
                        u, v = v, u
                    edge_key = u * 100000 + v
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        px1, py1 = points[u]
                        px2, py2 = points[v]
                        w = abs_func(px1 - px2) + abs_func(py1 - py2)
                        add_edge(Edge(u, v, w))
                        
    candidate_edges = []
    sorted_edges = sorted(grafo.edges())
    
    kruskal_uf = UnionFind(N)
    for i in range(N):
        x, y = points[i]
        orig_idx = coords_to_idx[(x, y)]
        if orig_idx != i:
            kruskal_uf.union(orig_idx, i)
            
    mst_weight = 0
    for aresta in sorted_edges:
        u = aresta.either()
        v = aresta.other(u)
        u_coord = points[u]
        v_coord = points[v]
        u_cell = u_coord[0] * grid_h + u_coord[1]
        v_cell = v_coord[0] * grid_h + v_coord[1]
        
        discovery_step = int(aresta.weight() / 2)
        
        accepted = kruskal_uf.union(u, v)
        if accepted:
            mst_weight += aresta.weight()
            
        candidate_edges.append({
            "u": u,
            "v": v,
            "weight": aresta.weight(),
            "accepted": accepted,
            "discovery_step": discovery_step
        })
        
    return {
        "grid_owners": owner,
        "grid_distances": dist,
        "candidate_edges": candidate_edges,
        "mst_weight": mst_weight
    }

class MainHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/solve':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                points_data = data.get('points', [])
                pontos = [(int(p[0]), int(p[1])) for p in points_data]
                
                result = solve_mst(pontos)
                response = {
                    "success": True,
                    **result
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                response = {
                    "success": False,
                    "error": str(e)
                }
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    os.chdir(root_path)
    server_address = ('', PORT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, MainHandler) as httpd:
        print(f"Servidor API/Web iniciado em http://localhost:{PORT}")
        print(f"Abra http://localhost:{PORT}/apresentacao.html no seu navegador")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor finalizado.")
