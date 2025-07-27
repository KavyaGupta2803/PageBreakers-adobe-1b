import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from collections import defaultdict

def extract_headings(doc, filename):
    headings = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if (
                        len(text) >= 10 and
                        span["size"] >= 12 and
                        text[0].isupper() and
                        not text.endswith(".")
                    ):
                        headings.append({
                            "document": filename,
                            "section_title": text,
                            "font_size": span["size"],
                            "page_number": page_num + 1
                        })
    return headings

def extract_snippets(doc, filename):
    snippets = []
    for page_num, page in enumerate(doc):
        text = page.get_text().strip().replace("\n", " ")
        if len(text) > 300:
            snippet = " ".join(text.split()[:100])
            snippets.append({
                "document": filename,
                "refined_text": snippet,
                "length": len(snippet),
                "page_number": page_num + 1
            })
    return snippets

def process_collection(collection_path):
    input_path = os.path.join(collection_path, "challenge1b_input.json")
    output_path = os.path.join(collection_path, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_path, "PDFs")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = data["documents"]
    persona = data["persona"]["role"]
    task = data["job_to_be_done"]["task"]
    timestamp = datetime.now().isoformat()

    all_headings = []
    all_snippets = []

    for doc in documents:
        filename = doc["filename"]
        pdf_path = os.path.join(pdf_dir, filename)

        if not os.path.exists(pdf_path):
            print(f"❌ Missing file: {filename}")
            continue

        try:
            doc_fitz = fitz.open(pdf_path)
            all_headings.extend(extract_headings(doc_fitz, filename))
            all_snippets.extend(extract_snippets(doc_fitz, filename))
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    # Group headings by document and pick top 2 per doc
    per_doc = defaultdict(list)
    for h in all_headings:
        per_doc[h["document"]].append(h)

    selected_headings = []
    for doc, hs in per_doc.items():
        top2 = sorted(hs, key=lambda x: -x["font_size"])[:2]
        selected_headings.extend(top2)

    # From all selected, pick top 5 globally
    final_headings = sorted(selected_headings, key=lambda x: -x["font_size"])[:5]
    extracted_sections = [
        {
            "document": h["document"],
            "section_title": h["section_title"],
            "importance_rank": i + 1,
            "page_number": h["page_number"]
        }
        for i, h in enumerate(final_headings)
    ]

    # Top 5 refined text snippets
    final_snippets = sorted(all_snippets, key=lambda x: -x["length"])[:5]
    subsection_analysis = [
        {
            "document": s["document"],
            "refined_text": s["refined_text"],
            "page_number": s["page_number"]
        }
        for s in final_snippets
    ]

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": timestamp
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Output saved to {output_path}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    collections = ["Collection 1", "Collection 2", "Collection 3"]

    for collection in collections:
        path = os.path.join(base, collection)
        if os.path.isdir(path):
            print(f"\n📂 Processing {collection}...")
            process_collection(path)
        else:
            print(f"⚠️ Skipped: {collection} folder not found.")
