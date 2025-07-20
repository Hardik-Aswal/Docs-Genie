import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator

def extract_headings_from_pdf(pdf_path):
    """
    Extracts title and headings (H1, H2, H3) from a PDF.
    This is a simplified approach based on font size.
    """
    doc = fitz.open(pdf_path)
    headings = []
    title = ""

    # Heuristic: Assume the largest font on the first page is the title
    if len(doc) > 0:
        first_page_fonts = sorted(list(set(s['size'] for b in doc[0].get_text("dict")['blocks'] if b['type'] == 0 for l in b['lines'] for s in l['spans'])), reverse=True)
        if first_page_fonts:
            title_font_size = first_page_fonts[0]
            # Find the first text block with this font size
            blocks = doc[0].get_text("dict")['blocks']
            for b in blocks:
                if b['type'] == 0:
                    for l in b['lines']:
                        for s in l['spans']:
                            if s['size'] == title_font_size:
                                title = s['text']
                                break
                        if title: break
                    if title: break

    # Extract headings from all pages
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:  # It's a text block
                for l in b['lines']:
                    for s in l['spans']:
                        font_size = s['size']
                        text = s['text'].strip()
                        if not text:
                            continue
                        
                        # Simple font-size based heuristic for headings
                        if 18 <= font_size < 24:
                            level = "H1"
                        elif 14 <= font_size < 18:
                            level = "H2"
                        elif 12 <= font_size < 14:
                            level = "H3"
                        else:
                            continue # Not a heading

                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })
    
    return {"title": title, "outline": headings}


def rank_sections_for_persona(doc_paths, persona_data):
    """
    Ranks document sections based on relevance to a persona's job description.
    """
    job_query = persona_data["job_to_be_done"]
    
    all_sections = []
    # Extract text from all sections of all documents
    for doc_path in doc_paths:
        doc = fitz.open(doc_path)
        for page_num, page in enumerate(doc):
            # A simplified way to get sections - could be improved
            headings = extract_headings_from_pdf(doc_path)["outline"]
            for heading in headings:
                if heading['page'] == page_num + 1:
                    all_sections.append({
                        "doc": os.path.basename(doc_path),
                        "page": page_num + 1,
                        "title": heading['text'],
                        "content": page.get_text() # Simplified: use full page text
                    })

    if not all_sections:
        return []

    # Use TF-IDF to find relevant sections
    section_contents = [section['content'] for section in all_sections]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(section_contents)
    query_vector = vectorizer.transform([job_query])

    # Calculate cosine similarity
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Add similarity score to each section
    for i, section in enumerate(all_sections):
        section['relevance'] = similarities[i]

    # Sort sections by relevance in descending order
    ranked = sorted(all_sections, key=operator.itemgetter('relevance'), reverse=True)

    # Format for output
    final_output = []
    for i, section in enumerate(ranked):
        final_output.append({
            "document": section['doc'],
            "page_number": section['page'],
            "section_title": section['title'],
            "importance_rank": i + 1,
            "refined_text": section['content'][:300] + "..." # Snippet
        })

    return final_output