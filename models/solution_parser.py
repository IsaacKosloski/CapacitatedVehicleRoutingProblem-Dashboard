import re

class SolutionParser:
    def parse_file(self, filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        # Padrões possíveis de custo
        patterns = [
            r'Cost\s*[:=]?\s*(\d+(?:\.\d+)?)',
            r'Custo\s*[:=]?\s*(\d+(?:\.\d+)?)',
            r'Total\s+Cost\s*[:=]?\s*(\d+(?:\.\d+)?)',
        ]

        cost = None
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                cost = float(match.group(1))
                break

        # Extrai rotas no formato "Route #1 : 1 2 3 4"
        routes = re.findall(r'Route\s+#?\d+\s*:\s*(.*)', content)
        routes = [list(map(int, r.strip().split())) for r in routes]

        return cost, routes


# 🔧 Função de utilidade para usar fora da classe
def extract_routes(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    routes = []
    for line in lines:
        if line.lower().startswith("route"):
            parts = line.split(":")
            if len(parts) > 1:
                route = list(map(int, parts[1].strip().split()))
                routes.append(route)
    return routes
