# this dummy_service pretends to be a server.serve_forever() simple
# python script for systemd testing. 
if __name__ == "__main__":
    import time

    while True:
        print("the sabot-receiver dummy service is alive")
        time.sleep(30)
