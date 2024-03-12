from plantuml import PlantUML

def generate_png(plantuml_code, output_file):
    plantuml = PlantUML()
    with open(output_file, "wb") as f:
        img = plantuml.processes(plantuml_code)
        f.write(img)

# Example usage
plantuml_code = """
@startuml
Bob -> Alice : hello
@enduml
"""

output_file = "output.png"
generate_png(plantuml_code, output_file)
print(f"PNG diagram saved as {output_file}")
