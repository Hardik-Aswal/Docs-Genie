# Docs-Genie
## Rethink Reading. Rediscover Knowledge 
What if every time you opened a PDF, it didn’t just sit there—it spoke to you, connected ideas, and narrated meaning across your entire library?  That’s the future I'm building!!!

# Adobe India Hackathon 2025: Connecting the Dots

This project is a unified solution for the Adobe India Hackathon 2025, handling the requirements for both Round 1A and Round 1B.

## 🚀 How to Run

1.  **Place Input Files**: Add your PDFs to the `/input` directory. For Round 1B, also include a `persona.json` file.
2.  **Build the Docker Image**:
    ```bash
    docker build -t adobe-hackathon .
    ```
3.  **Run the Container**:
    ```bash
    docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe-hackathon
    ```

## Approach

### Document Outlining
The script processes PDFs to identify hierarchical structures. It analyzes text properties like font size and position to distinguish between different heading levels (H1, H2, H3) and extracts the document's title.

### Persona-Driven Analysis
For this round, the solution uses the structured outline from Round 1A and performs a semantic analysis based on the provided persona and job description. It ranks sections by relevance to provide a prioritized list of insights.

## Libraries Used
* PyMuPDF (fitz)
* scikit-learn (for TF-IDF vectorization)