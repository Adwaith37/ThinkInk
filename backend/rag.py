from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_namespace(user_id: str) -> str:
    """Each user gets their own namespace in Pinecone"""
    return user_id.replace("-", "_")

def add_example_to_rag(user_id: str, blog: str, example_id: str,
                        category: str = "opinion", style: str = "analytical",
                        has_personal_voice: bool = False):
    embedding = embedding_model.encode(blog[:1000]).tolist()
    index.upsert(
        vectors=[{
            "id": example_id,
            "values": embedding,
            "metadata": {
                "blog": blog[:2000],
                "user_id": user_id,
                "category": category,
                "style": style,
                "has_personal_voice": has_personal_voice
            }
        }],
        namespace=get_namespace(user_id)
    )
    print(f"✅ Added example to Pinecone for {user_id} [category={category}, personal_voice={has_personal_voice}]")
    
    print(f"✅ Added example to Pinecone for {user_id}")

def retrieve_relevant_examples(user_id: str, topic: str, category: str = None,
                                prefer_personal_voice: bool = False, top_k: int = 3) -> list:
    try:
        topic_embedding = embedding_model.encode(topic).tolist()

        # Build metadata filter if category is known
        filter_dict = {}
        if category:
            filter_dict["category"] = {"$eq": category}

        results = index.query(
            vector=topic_embedding,
            top_k=top_k * 2 if prefer_personal_voice else top_k,  # over-fetch slightly so we can re-rank
            namespace=get_namespace(user_id),
            include_metadata=True,
            filter=filter_dict if filter_dict else None
        )

        if not results or not results["matches"]:
            return []

        matches = results["matches"]

        # If personal voice is requested, soft-prefer matches that have it
        if prefer_personal_voice:
            matches.sort(
                key=lambda m: m["metadata"].get("has_personal_voice", False),
                reverse=True
            )

        top_matches = matches[:top_k]
        return [match["metadata"]["blog"] for match in top_matches]

    except Exception as e:
        print(f"Pinecone query error: {e}")
        return []

def delete_oldest_if_limit(user_id: str, max_examples: int = 8):
    try:
        namespace = get_namespace(user_id)
        stats = index.describe_index_stats()
        ns_stats = stats.get("namespaces", {}).get(namespace, {})
        count = ns_stats.get("vector_count", 0)

        if count >= max_examples:
            # Fetch all vectors and delete oldest
            results = index.list(namespace=namespace)
            ids = list(results)
            if ids:
                oldest_id = sorted(ids)[0]
                index.delete(ids=[oldest_id], namespace=namespace)
                print(f"🗑️ Deleted oldest example for {user_id}")
    except Exception as e:
        print(f"Pinecone delete error: {e}")

def get_example_count(user_id: str) -> int:
    try:
        namespace = get_namespace(user_id)
        stats = index.describe_index_stats()
        return stats.get("namespaces", {}).get(namespace, {}).get("vector_count", 0)
    except:
        return 0