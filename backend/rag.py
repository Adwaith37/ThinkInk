from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

def get_index():
    return pc.Index(index_name)

def get_namespace(user_id: str) -> str:
    """Each user gets their own namespace in Pinecone"""
    return user_id.replace("-", "_")

def add_example_to_rag(user_id: str, blog: str, example_id: str,
                        category: str = "opinion", style: str = "analytical",
                        has_personal_voice: bool = False):
    """Add example using Pinecone hosted embeddings"""
    index = get_index()
    
    index.upsert_records(
        namespace=get_namespace(user_id),
        records=[{
            "_id": example_id,
            "text": blog[:1000],
            "category": category,
            "style": style,
            "has_personal_voice": has_personal_voice,
            "user_id": user_id
        }]
    )
    print(f" Added example to Pinecone for {user_id} [category={category}]")

def retrieve_relevant_examples(user_id: str, topic: str, category: str = None,
                                prefer_personal_voice: bool = False,
                                top_k: int = 3) -> list:
    """Retrieve relevant examples using Pinecone hosted embeddings"""
    try:
        index = get_index()
        namespace = get_namespace(user_id)

        # Build filter
        filter_dict = {}
        if category:
            filter_dict["category"] = {"$eq": category}

        n_results = top_k * 2 if prefer_personal_voice else top_k

        results = index.search(
            namespace=namespace,
            query={
                "inputs": {"text": topic},
                "top_k": n_results,
                "filter": filter_dict if filter_dict else None
            },
            fields=["text", "category", "style", "has_personal_voice"]
        )

        matches = results.get("result", {}).get("hits", [])

        if not matches:
            return []

        # Soft-prefer personal voice if requested
        if prefer_personal_voice:
            matches.sort(
                key=lambda m: m.get("fields", {}).get("has_personal_voice", False),
                reverse=True
            )

        top_matches = matches[:top_k]
        return [m.get("fields", {}).get("text", "") for m in top_matches]

    except Exception as e:
        print(f"Pinecone query error: {e}")
        return []

def delete_oldest_if_limit(user_id: str, max_examples: int = 8):
    """Delete oldest example if limit exceeded"""
    try:
        index = get_index()
        namespace = get_namespace(user_id)

        results = index.list(namespace=namespace)
        ids = list(results)

        if len(ids) >= max_examples:
            oldest_id = sorted(ids)[0]
            index.delete(ids=[oldest_id], namespace=namespace)
            print(f" Deleted oldest example for {user_id}")
    except Exception as e:
        print(f"Pinecone delete error: {e}")

def get_example_count(user_id: str) -> int:
    """Get number of examples stored for user"""
    try:
        index = get_index()
        namespace = get_namespace(user_id)
        stats = index.describe_index_stats()
        return stats.get("namespaces", {}).get(namespace, {}).get("vector_count", 0)
    except:
        return 0