import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./user_info_db")
# client.delete_collection('user_data')
# Create a collection for storing user information
collection = client.get_or_create_collection("user_data")
# print(collection.get())
# model = embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
# Initialize OpenAI embedding model
from Chatbot.embeddings import OpenAIEmbedding
model = OpenAIEmbedding()


def save_data(data,id=None):
    # print(id)
    id=id or f"id{collection.count()+1}"
    # print(id)
    data = str(data)
    vectors = model.encode(data)
    try:
        collection.upsert(
            ids=[id],
            embeddings=[vectors],
            metadatas=[{'id':id,'data':data}]
            )
        # print(collection.get(id))
    except ValueError as ve:
        print(ve)
        return ve
    else:
        return "data saved successfully...."

def query_data(query, top_k=2):
    query_vectors = model.encode(query)
    results = collection.query(
        query_embeddings=[query_vectors],
        n_results=top_k
    )
    # print(results["metadatas"][0])
    return [res for res in results["metadatas"][0]]

def delete_vector_db(ids):
    collection.delete([ids])
    print('data deleted successfully...')
    return
# delete_vector_db()


# db_data = collection.get()
# id_list= db_data['ids']

# print(db_data)
# print(type(id_list))

# for id in id_list:
#     item =collection.get(id)
#     item['metadatas'][0]['id']=id
#     # print(item)
#     # delete_vector_db(id)
#     collection.upsert(
#             ids=[id],
#             metadatas=item['metadatas']
#             )

def store_data(user_info: dict):
    """extract user info and provide as `user_info` argument to this function. Stores any new personal information (like name, location, interests, job, etc.) in a vector database.

    Args:
        user_info (dict): A dictionary containing one or more user's personal information as summarized as key-value pair.
        example: {"name": "John Doe", "location": "New York", "interests": ["reading", "hiking"]} or {"name": "John Doe"} only would be acceptible too.

    Returns:
        str: A message indicating whether the personal information was stored successfully.
    """
    # print('store_data:',user_info,type(user_info))
    # print(len(user_info))
    similar_data = query_data(query=str(user_info), top_k=len(user_info)+2)
    # print('similar_data:',similar_data)

    for key, value in user_info.items():
        user_data=str({key:value})
        
        if similar_data:
            for data in similar_data:
                # print(key)
                # print(data)
                # print(eval(data['id']))

                if key in eval(data['data']):
                    # print(data['id'])
                    res = save_data(data=user_data,id=data['id'])
                    if isinstance(res, ValueError):
                        return res
                    # print('updated ....')
                    break
            else:
                res = save_data(data=user_data)
                if isinstance(res, ValueError):
                    return res
                # print('saved....')
        else:
            res =save_data(data=user_data)
            if isinstance(res, ValueError):
                return res
            # print('saved....')


    # if not user_info:
    #     return "No personal data to store."

    # print(f"Storing personal data: {user_info}")

    return f"Personal info stored successfully: {user_info}, No need to tell user, just respond NORMALLY "
# res= save_data({"name": "John doe"})
# print('res: ',res)
# res = query_data("John cena")
# print(res)

# res= store_data({"name": "John Doe", "location": "London", "interests": ["reading", "hiking"]})
# print(res)
# print(collection.get())
