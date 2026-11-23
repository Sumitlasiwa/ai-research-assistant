# visualize_graph.py
from app.workflows.research_graph import build_research_graph

def save_graph_visualization():
    # Generate the PNG bytes
    png_data = build_research_graph().get_graph().draw_mermaid_png()
    
    # Save to file
    output_path = "workflow_graph.png"
    with open(output_path, "wb") as f:
        f.write(png_data)
    
    print(f"✅ Graph saved successfully to {output_path}")

if __name__ == "__main__":
    save_graph_visualization()   