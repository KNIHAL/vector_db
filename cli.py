from core.vectordb import VectorDB
from core.loaders import load_pdf, load_txt, load_md
from core.chunker import chunk_text
import os

db = VectorDB()

def menu():
    print("\n--- Vector DB CLI ---")
    print("1. Add text")
    print("2. Search text")
    print("3. Delete by id")
    print("4. Ingest file (PDF / MD / TXT)")
    print("5. Exit")

while True:
    menu()
    choice = input("Choose option: ").strip()

    # ---------------- Add text ----------------
    if choice == "1":
        text = input("Enter text: ")
        meta_type = input("Metadata type (optional): ")
        metadata = {"type": meta_type} if meta_type else {}
        rid = db.insert(text, metadata)
        print("Inserted with id:", rid)

    # ---------------- Search ----------------
    elif choice == "2":
        query = input("Enter search query: ")
        k = input("Top K results (default 3): ").strip()
        top_k = int(k) if k.isdigit() else 3

        results = db.search(query, top_k=top_k)
        for score, record in results:
            print(f"\nScore: {score:.4f}")
            print("ID:", record["id"])
            print("Text:", record["text"])
            print("Metadata:", record["metadata"])

    # ---------------- Delete ----------------
    elif choice == "3":
        rid = input("Enter record id to delete: ")
        db.delete(rid)
        print("Delete attempted.")

    # ---------------- Ingest file ----------------
    elif choice == "4":
        path = input("Enter file path: ").strip()
        if not os.path.exists(path):
            print("File not found.")
            continue

        save = input("Save file for future use? (y/n): ").lower() == "y"
        ext = os.path.splitext(path)[1].lower()

        if save:
            os.makedirs("data/uploads", exist_ok=True)
            dest = f"data/uploads/{os.path.basename(path)}"
            with open(path, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            path = dest

        if ext == ".txt":
            text = load_txt(path)
        elif ext == ".md":
            text = load_md(path)
        elif ext == ".pdf":
            text = load_pdf(path)
        else:
            print("Unsupported file type.")
            continue

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            db.insert(
                chunk,
                {
                    "source": os.path.basename(path),
                    "stored": save,
                    "chunk_id": i
                }
            )

        print(f"Ingested {len(chunks)} chunks | stored={save}")

    # ---------------- Exit ----------------
    elif choice == "5":
        print("Exiting Vector DB.")
        break

    else:
        print("Invalid option.")
