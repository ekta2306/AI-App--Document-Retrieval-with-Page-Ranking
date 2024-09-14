import query as q

def get_query():
    # Get query from user
    user_query = input("Enter your query: ")

    # Process the query
    result = q.process_query(user_query)

    # Display the result
    print("Best matching document:")
    print(result)