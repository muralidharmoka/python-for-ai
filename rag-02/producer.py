import redis
import uuid

#redis set up
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
#send payload to queue ( provide id and query)
def send_to_queue(query): 
    job_id = str(uuid.uuid4())  # Generate a unique ID for the query   
    payload = {
        "id": job_id,  # Use the generated job ID
        "query": query
    }
    redis_client.rpush("query_queue", str(payload))  # Push the payload to the Redis list (queue)
    return job_id

user_query = input("HUMAN INPUT: ")
job_id = send_to_queue(user_query)  

print(f"Query sent to queue with Job ID: {job_id} Successfully!")