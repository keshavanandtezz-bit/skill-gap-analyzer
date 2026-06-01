# =============================================================================
# SKILL GAP ANALYZER - Charts & Visualizations Module
# =============================================================================
# This module creates beautiful interactive charts using Plotly.
# All charts use a dark, consistent color theme.

import plotly.graph_objects as go
import plotly.express as px


# ── Color Palette ─────────────────────────────────────────────────────────────
COLORS = {
    "matched":   "#00D4AA",   # Teal green (success)
    "missing":   "#FF5C7A",   # Vibrant red (danger)
    "extra":     "#7C83FF",   # Soft purple (bonus)
    "bg":        "#0E1117",   # Dark background
    "card":      "#1A1D2E",   # Card background
    "text":      "#E8EAF6",   # Light text
    "accent":    "#6C63FF",   # Primary accent purple
    "grid":      "#2A2D3E",   # Grid lines
}


def create_donut_chart(matched: int, missing: int, extra: int) -> go.Figure:
    """
    Create an animated donut chart showing skill distribution.
    
    Sections:
    - Matched: skills found in both resume and JD
    - Missing: skills the JD requires but resume lacks
    - Extra: resume skills not in JD (bonus skills)
    """
    labels = ["✅ Matched", "❌ Missing", "⭐ Extra (Bonus)"]
    values = [matched, missing, extra]
    colors = [COLORS["matched"], COLORS["missing"], COLORS["extra"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,                          # Makes it a donut chart
        marker=dict(
            colors=colors,
            line=dict(color=COLORS["bg"], width=3)
        ),
        textinfo="label+percent",
        textfont=dict(size=13, color=COLORS["text"]),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
        pull=[0.05, 0.05, 0.0],            # Slightly pull matched & missing
    )])

    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"], family="Inter, sans-serif"),
        margin=dict(t=30, b=30, l=30, r=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        showlegend=True,
        height=340,
    )

    return fig


def create_category_bar_chart(category_breakdown: list) -> go.Figure:
    """
    Create a horizontal grouped bar chart showing per-category match %.
    
    Each bar shows how many skills in that category were matched vs. required.
    """
    if not category_breakdown:
        return go.Figure()

    categories = [item["category"] for item in category_breakdown]
    scores = [item["score"] for item in category_breakdown]
    matched = [item["matched"] for item in category_breakdown]
    required = [item["required"] for item in category_breakdown]

    # Color bars based on score (green → red gradient)
    bar_colors = []
    for s in scores:
        if s >= 70:
            bar_colors.append(COLORS["matched"])
        elif s >= 40:
            bar_colors.append("#FFB347")   # Orange for mid range
        else:
            bar_colors.append(COLORS["missing"])

    fig = go.Figure()

    # Background bar (total = 100%)
    fig.add_trace(go.Bar(
        y=categories,
        x=[100] * len(categories),
        orientation="h",
        marker=dict(color=COLORS["grid"]),
        hoverinfo="skip",
        showlegend=False,
        name="Total"
    ))

    # Foreground bar (score %)
    fig.add_trace(go.Bar(
        y=categories,
        x=scores,
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(color=COLORS["bg"], width=1)
        ),
        text=[f"{s}%  ({m}/{r})" for s, m, r in zip(scores, matched, required)],
        textposition="inside",
        textfont=dict(color=COLORS["bg"], size=11, family="Inter"),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}%<extra></extra>",
        name="Match %",
    ))

    fig.update_layout(
        barmode="overlay",
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"], family="Inter, sans-serif"),
        margin=dict(t=20, b=20, l=10, r=80),
        xaxis=dict(
            title="Match Percentage (%)",
            range=[0, 115],
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["grid"],
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            tickfont=dict(size=12),
        ),
        height=max(300, len(categories) * 55),
        showlegend=False,
    )

    return fig


def create_gauge_chart(score: float, grade: str) -> go.Figure:
    """
    Create a speedometer-style gauge chart for the overall match score.
    
    The gauge arc changes color based on score:
    - 0-40%   Red zone (Poor match)
    - 40-70%  Yellow zone (Partial match)
    - 70-100% Green zone (Strong match)
    """
    # Determine color based on score
    if score >= 70:
        color = COLORS["matched"]
        label = "Strong Match 🚀"
    elif score >= 40:
        color = "#FFB347"
        label = "Partial Match ⚡"
    else:
        color = COLORS["missing"]
        label = "Needs Work 📚"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number=dict(
            suffix="%",
            font=dict(size=44, color=color, family="Inter")
        ),
        delta=dict(
            reference=70,
            increasing=dict(color=COLORS["matched"]),
            decreasing=dict(color=COLORS["missing"]),
            font=dict(size=16)
        ),
        title=dict(
            text=f"<b>{label}</b><br><span style='font-size:24px;color:#9CA3AF'>Grade: {grade}</span>",
            font=dict(size=18, color=COLORS["text"], family="Inter")
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=2,
                tickcolor=COLORS["text"],
                tickfont=dict(size=12, color=COLORS["text"])
            ),
            bar=dict(color=color, thickness=0.25),
            bgcolor=COLORS["card"],
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color="#2D1B24"),
                dict(range=[40, 70], color="#2D2A1B"),
                dict(range=[70, 100], color="#1B2D28"),
            ],
            threshold=dict(
                line=dict(color=COLORS["text"], width=3),
                thickness=0.8,
                value=score
            )
        )
    ))

    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"], family="Inter, sans-serif"),
        margin=dict(t=20, b=20, l=40, r=40),
        height=300,
    )

    return fig


def create_radar_chart(category_breakdown: list) -> go.Figure:
    """
    Create a radar/spider chart showing multi-dimensional skill coverage.
    
    Each axis represents a job requirement category.
    The area filled shows how well the resume covers each dimension.
    """
    if len(category_breakdown) < 3:
        return None   # Radar chart needs at least 3 axes

    # Use short category names (strip emoji prefix)
    short_names = []
    for item in category_breakdown:
        name = item["category"]
        # Keep just the text part after the emoji
        parts = name.split(" ", 1)
        short_names.append(parts[1] if len(parts) > 1 else name)

    scores = [item["score"] for item in category_breakdown]

    # Close the radar by repeating the first value
    scores_closed = scores + [scores[0]]
    names_closed = short_names + [short_names[0]]

    fig = go.Figure()

    # Filled area (resume coverage)
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=names_closed,
        fill="toself",
        fillcolor=f"rgba(108, 99, 255, 0.3)",
        line=dict(color=COLORS["accent"], width=2),
        name="Your Coverage",
        hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>"
    ))

    # Target line at 100%
    full = [100] * len(names_closed)
    fig.add_trace(go.Scatterpolar(
        r=full,
        theta=names_closed,
        fill="toself",
        fillcolor="rgba(255,255,255,0.03)",
        line=dict(color=COLORS["grid"], width=1, dash="dot"),
        name="Target (100%)",
        hoverinfo="skip"
    ))

    fig.update_layout(
        polar=dict(
            bgcolor=COLORS["card"],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=COLORS["text"]),
                gridcolor=COLORS["grid"],
                linecolor=COLORS["grid"],
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=COLORS["text"]),
                gridcolor=COLORS["grid"],
                linecolor=COLORS["grid"],
            )
        ),
        paper_bgcolor=COLORS["card"],
        font=dict(color=COLORS["text"], family="Inter, sans-serif"),
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(size=12)
        ),
        margin=dict(t=30, b=50, l=60, r=60),
        height=400,
        showlegend=True,
    )

    return fig
