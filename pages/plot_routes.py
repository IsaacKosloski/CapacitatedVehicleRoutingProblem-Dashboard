import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go

def plot_routes_plotly(routes, coords, highlight_index=None):
    fig = go.Figure()

    depot = routes[0][0]
    depot_x, depot_y = coords[depot]

    fig.add_trace(go.Scatter(
        x=[depot_x], y=[depot_y],
        mode="markers+text",
        name="Depósito",
        marker=dict(size=12, color="red", symbol="star"),
        text=["Depósito"],
        textposition="top center"
    ))

    # Paleta de cores para rotas distintas
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b",
              "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#d62728"]

    for i, route in enumerate(routes):
        x_vals = [coords[n][0] for n in route] + [coords[route[0]][0]]
        y_vals = [coords[n][1] for n in route] + [coords[route[0]][1]]

        if highlight_index is None:
            # Todas coloridas normalmente
            color = colors[i % len(colors)]
            opacity = 1.0
            width = 3
        else:
            is_highlight = (i == highlight_index)
            color = colors[i % len(colors)] if is_highlight else "#d3d3d3"
            opacity = 1.0 if is_highlight else 0.3
            width = 4 if is_highlight else 2

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers",
            name=f"Rota {i+1}",
            line=dict(width=width, color=color),
            marker=dict(size=6, color=color),
            opacity=opacity,
            hoverinfo="text",
            text=[f"Rota {i+1}"] * len(x_vals)
        ))

    fig.update_layout(
        title="Visualização de Rotas (Interativa)",
        xaxis_title="Coordenada X",
        yaxis_title="Coordenada Y",
        legend_title="Rotas",
        showlegend=True,
        width=900,
        height=600
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
