import psycopg2

def create_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="prompts_db",
        user="your_username",
        password="your_password"
    )

    return conn

def add_prompt(conn, prompt):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO prompts (prompt_text) VALUES (%s) RETURNING id", (prompt,))
        prompt_id = cur.fetchone()[0]
    conn.commit()
    return prompt_id

def add_text_result(conn, prompt_id, result_text):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO results (prompt_id, type, result_text) VALUES (%s, %s, %s)", (prompt_id, 'text', result_text))
    conn.commit()

def add_image_result(conn, prompt_id, image_file):
    with open(image_file, 'rb') as f:
        image_data = f.read()

    with conn.cursor() as cur:
        cur.execute("INSERT INTO results (prompt_id, type, image) VALUES (%s, %s, %s)", (prompt_id, 'image', psycopg2.Binary(image_data)))
    conn.commit()

def add_code_result(conn, prompt_id, code):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO results (prompt_id, type, code) VALUES (%s, %s, %s)", (prompt_id, 'code', code))
    conn.commit()

def main():
    # create a connection to the database
    conn = create_conn()

    prompts_and_results = [
        {
            "prompt": "Write a short story.",
            "result_type": "text",
            "result": "Once upon a time..."
        },
        {
            "prompt": "Draw a picture.",
            "result_type": "image",
            "result": "/path/to/your/image.jpg"
        },
        {
            "prompt": "Write a Python script.",
            "result_type": "code",
            "result": "print('Hello, world!')"
        },
        # add more prompts and results here...
    ]

    for pr in prompts_and_results:
        prompt_id = add_prompt(conn, pr["prompt"])

        if pr["result_type"] == "text":
            add_text_result(conn, prompt_id, pr["result"])
        elif pr["result_type"] == "image":
            add_image_result(conn, prompt_id, pr["result"])
        elif pr["result_type"] == "code":
            add_code_result(conn, prompt_id, pr["result"])

if __name__ == "__main__":
    main()
