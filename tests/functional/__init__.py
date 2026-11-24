def login(client, username, password, next_path):
    return client.post("/connexion/",
                       data={"Login": username, "Password": password, "next": next_path},
                       follow_redirects=True)
