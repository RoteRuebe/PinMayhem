def main():
    with open("token.txt","rt") as f:
        token = new_token(f.read())
        
    with open("token.txt","wt") as f:
        f.write(token)
        
    return token
        
        
def new_token(last_token):
    return(str(int(last_token)+1))
