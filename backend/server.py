from flask import Flask, request
from config import connect_to_mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/home")
def home():
    return {"msg": "Hello"}

@app.route("/api/posts", methods=["GET", "POST"])
def products():
    connection = connect_to_mysql()
    cursor = connection.cursor(buffered=True)
    if request.method == "GET":
        try:
            query = "SELECT * FROM posts"
            cursor.execute(query)
            formatedPosts = []
            posts = cursor.fetchall()
            for post in posts:
                post_object = {
                    "id": post[0],
                    "userId": post[1],
                    "title": post[2],
                    "content": post[3],
                    "createdAt": post[4],
                    "updatedAt": post[5]
                }

                formatedPosts.append(post_object)

            return {"posts": formatedPosts}, 200
        except Exception as err:
            print(f"Error retrieving data: {err}")
            return 'Error retrieving data!', 500
        finally:
            if connection:
                print("Connection closed")
                connection.close()
    elif request.method == "POST":
        data = request.get_json()
        print(data)
        user_id = data.get("userId")
        title = data.get("title")
        content = data.get("content")

        post = {
            "user_id": user_id,
            "title": title,
            "content": content
        }

    try:
        query = "INSERT INTO posts (user_id, title, content) VALUES(%s, %s, %s)"
        values = (user_id, title, content)

        cursor.execute(query, values)
        connection.commit()

        return {"post": post}, 200
    except Exception as err:
            print(f"Error inserting data: {err}")
            return 'Error inserting data!', 500
    finally:
        if connection:
            print("Connection closed")
            connection.close()

if __name__=="__main__":
    app.run(port=7090, debug=True)