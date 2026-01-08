from core.vectordb import VectorDB

db = VectorDB()

def menu():
    print("\n--- Vector DB CLI ---")
    print("1. Add text")
    print("2. Search text")
    print("3. Delete by id")
    print("4. Exit")

while True:
    menu()
    choice = input("Choose option: ").strip()

    if choice == "1":
        text = input("Enter text: ")
        meta_type = input("Metadata type (optional): ")
        metadata = {"type": meta_type} if meta_type else {}
        rid = db.insert(text, metadata)
        print("Inserted with id:", rid)

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

    elif choice == "3":
        rid = input("Enter record id to delete: ")
        db.delete(rid)
        print("Delete attempted (check search to confirm).")

    elif choice == "4":
        print("Exiting Vector DB.")
        break

    else:
        print("Invalid option.")
