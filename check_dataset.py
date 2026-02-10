from pymongo import MongoClient

# -----------------------------
# 1. Connect to MongoDB
# -----------------------------
client = MongoClient("localhost:27017")  # change if you have a remote URI
db = client.datasets                   # your database
collection = db.datasets_law           # your collection

# -----------------------------
# 2. Count total documents
# -----------------------------
total_docs = collection.count_documents({})
print(f"Total documents in collection: {total_docs}\n")

# -----------------------------
# 3. Sample first 5 documents
# -----------------------------
print("=== Sample 5 documents ===")
for i, doc in enumerate(collection.find().limit(5)):
    print(f"Document {i+1}:")
    print(f"Title: {doc.get('title', '')}")
    print(f"Article Number: {doc.get('article_number', '')}")
    print(f"Page: {doc.get('page', '')}")
    print(f"Law Reference: {doc.get('law_reference', '')}")
    print(f"Text Preview: {doc.get('text', '')[:200]}...")  # first 200 chars
    print("---")

# -----------------------------
# 4. Find documents with empty or missing 'text'
# -----------------------------
empty_text_docs = collection.count_documents({"text": {"$eq": ""}})
print(f"\nDocuments with empty 'text' field: {empty_text_docs}")

# Optionally, list them
if empty_text_docs > 0:
    print("Listing documents with empty text:")
    for doc in collection.find({"text": {"$eq": ""}}):
        print(f"Article {doc.get('article_number', 'N/A')} - Title: {doc.get('title', '')}")

# -----------------------------
# 5. Check for missing fields
# -----------------------------
required_fields = ['title', 'article_number', 'text', 'page', 'law_reference']
missing_fields_docs = {field: collection.count_documents({field: {"$exists": False}}) for field in required_fields}
print("\nMissing fields summary:")
for field, count in missing_fields_docs.items():
    print(f"{field}: {count} documents missing")

# -----------------------------
# 6. Optional: Search for keyword
# -----------------------------
keyword = "مؤسسة ناشئة"
print(f"\nDocuments containing keyword '{keyword}':")
for doc in collection.find({"text": {"$regex": keyword}}).limit(5):
    print(f"- Article {doc.get('article_number', '')} - {doc.get('title', '')}")
