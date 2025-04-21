import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go


def plot_routes_plotly(routes, coords):
    fig = go.Figure()

    # Identifica o depósito
    depot = routes[0][0]
    depot_x = coords[depot][0]
    depot_y = coords[depot][1]

    # Adiciona o marcador do depósito primeiro
    fig.add_trace(go.Scatter(
        x=[depot_x],
        y=[depot_y],
        mode="markers+text",
        name="Depósito",
        marker=dict(color='red', size=12, symbol='star'),
        text=["Depósito"],
        textposition="top center"
    ))

    # Adiciona as rotas
    for i, route in enumerate(routes):
        x_vals = [coords[n][0] for n in route]
        y_vals = [coords[n][1] for n in route]
        x_vals.append(x_vals[0])
        y_vals.append(y_vals[0])

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers",
            name=f"Rota {i+1}"
        ))

    fig.update_layout(
        title="Rotas (Plotly)",
        xaxis_title="X",
        yaxis_title="Y",
        width=800,
        height=600,
        legend_title="Legenda",
    )
    return fig



def plot_routes_folium(routes, coords):
    depot = routes[0][0]
    depot_coords = coords[depot]
    m = folium.Map(location=[depot_coords[1], depot_coords[0]], zoom_start=13)

    colors = ["red", "blue", "green", "purple", "orange", "black", "pink", "gray", "cyan", "brown"]

    for i, route in enumerate(routes):
        route_coords = [(coords[n][1], coords[n][0]) for n in route]
        folium.PolyLine(
            locations=route_coords,
            color=colors[i % len(colors)],
            weight=4,
            opacity=0.7,
            tooltip=f"Rota {i+1}"
        ).add_to(m)

        for j, node in enumerate(route_coords):
            folium.CircleMarker(location=node, radius=3, fill=True).add_to(m)

    # Adiciona o marcador do depósito (destacado)
    folium.Marker(
        location=(depot_coords[1], depot_coords[0]),
        popup="Depósito",
        tooltip="Depósito",
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)

    folium_static(m)
