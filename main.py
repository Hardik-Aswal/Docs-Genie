import os
import json
from datetime import datetime
from utils import extract_headings_from_pdf, rank_sections_for_persona

def documentOutline(pdf_path, output_dir):
    """
    Executes the logic for Round 1A: extracting a document outline.
    """
    print(f"Running Round 1A for {os.path.basename(pdf_path)}...")
    data = extract_headings_from_pdf(pdf_path)

    # Create a JSON output file for the PDF
    output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".json"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully generated outline at {output_path}")

def documentAnalysis(input_dir, output_dir):
    """
    Executes the logic for Round 1B: persona-driven analysis.
    """
    print("Running Round 1B...")
    persona_path = os.path.join(input_dir, "persona.json")

    if not os.path.exists(persona_path):
        print("persona.json not found. Skipping Round 1B.")
        return

    with open(persona_path, 'r') as f:
        persona_data = json.load(f)

    documents = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".pdf")]
    
    # Get ranked sections based on persona
    ranked_sections = rank_sections_for_persona(documents, persona_data)

    # Prepare the output
    output_data = {
        "metadata": {
            "input_documents": [os.path.basename(doc) for doc in documents],
            "persona": persona_data["persona"],
            "job_to_be_done": persona_data["job_to_be_done"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "results": ranked_sections
    }
    
    output_path = os.path.join(output_dir, "round_1b_output.json")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Successfully generated persona analysis at {output_path}")


if __name__ == "__main__":
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"

    # Determine which round to run based on the presence of persona.json
    if os.path.exists(os.path.join(INPUT_DIR, "persona.json")):
        # If persona file exists, run Round 1B
        documentAnalysis(INPUT_DIR, OUTPUT_DIR)
    else:
        # Otherwise, run Round 1A on all PDFs
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(INPUT_DIR, filename)
                documtnee(pdf_path, OUTPUT_DIR)