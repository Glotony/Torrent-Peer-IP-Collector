import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()


QB_URL = os.getenv("QB_URL")
USERNAME = os.getenv("QB_USERNAME")
PASSWORD = os.getenv("QB_PASSWORD")

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    "scraped_ips"
)

IP_LIMIT = int(
    os.getenv(
        "IP_LIMIT",
        "100"
    )
)


session = requests.Session()



def login():

    response = session.post(
        f"{QB_URL}/api/v2/auth/login",
        data={
            "username": USERNAME,
            "password": PASSWORD
        }
    )

    if response.status_code not in (200, 204):
        raise Exception(
            f"Login failed: HTTP {response.status_code}"
        )



def get_torrents():

    response = session.get(
        f"{QB_URL}/api/v2/torrents/info"
    )

    return response.json()



def get_peers(torrent_hash):

    response = session.get(
        f"{QB_URL}/api/v2/sync/torrentPeers",
        params={
            "hash": torrent_hash
        }
    )

    data = response.json()

    peers = data.get(
        "peers",
        {}
    )

    return [
        peer["ip"]
        for peer in peers.values()
        if "ip" in peer
    ]



def load_ips():

    ips = set()

    if not os.path.exists(OUTPUT_DIR):
        return ips


    for file in os.listdir(OUTPUT_DIR):

        if file.endswith(".json"):

            with open(
                os.path.join(
                    OUTPUT_DIR,
                    file
                ),
                "r"
            ) as f:

                ips.update(
                    json.load(f)
                )

    return ips



def save_ips(new_ips):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    ips = load_ips()

    ips.update(
        new_ips
    )

    ips = list(ips)


    for index in range(
        0,
        len(ips),
        IP_LIMIT
    ):

        number = (
            index // IP_LIMIT
        ) + 1


        with open(
            os.path.join(
                OUTPUT_DIR,
                f"ips_{number}.json"
            ),
            "w"
        ) as f:

            json.dump(
                ips[index:index + IP_LIMIT],
                f,
                indent=4
            )



def main():

    login()


    while True:

        torrents = get_torrents()

        ips = []


        for torrent in torrents:

            ips.extend(
                get_peers(
                    torrent["hash"]
                )
            )


        if ips:

            save_ips(
                ips
            )



if __name__ == "__main__":

    main()