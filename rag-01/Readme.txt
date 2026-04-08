compose.yaml
  #services:
  vector-db:
    image: docker.io/qdrant/qdrant:latest
    ports:
      - 6333:6333

What the lines above mean (line by line)
    You are telling Docker:
👉 “I want to run some services (containers)”

#🔹 vector-db:
    This is just a name you gave
    Think of it like: "database container name"

#🔹 image: docker.io/qdrant/qdrant:latest
This is the most important line.

👉 It tells Docker:

    “Download and run Qdrant (vector database) from Docker Hub”

    So behind the scenes:

    Docker pulled this image from internet
    Created a container
    Started Qdrant server inside it

“Download and run Qdrant (vector database) from Docker Hub”

    - 6333:6333  : This means Your PC port 6333  →  Container port 6333

#Summary
   You have successfully:
    ✅ Started Docker container
    ✅ Exposed port 6333
    ✅ Qdrant is running
    ✅ Dashboard is accessible
 #Qdrant Desktop URL : http://localhost:6333/dashboard#/welcome

#Commands
  />docker compose up -d #starts the container in background and also maps the port
  />docker compose ps