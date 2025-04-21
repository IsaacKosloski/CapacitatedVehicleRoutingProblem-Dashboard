def get_coordinates_from_vrp(filepath):
    coords = {}
    reading = False
    with open(filepath, "r") as file:
        for line in file:
            if "NODE_COORD_SECTION" in line:
                reading = True
                continue
            if "DEMAND_SECTION" in line:
                break
            if reading:
                parts = line.strip().split()
                if len(parts) >= 3:
                    node_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coords[node_id] = (x, y)
    return coords
