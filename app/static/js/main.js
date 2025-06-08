let peers;

function createSpan(text) {
    let span = document.createElement('span');
    span.textContent = text;
    return span;
}

async function makePeersTable() {
    try {
        const response = await fetch("/api/peers", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        });

        const result = await response.json();
        peers = result;
        console.log("Server response:", result);

        let status;
        for (let peer of peers) {
            try {
                const response = await fetch("/api/peer_status", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                });
                status = await response.json();
            }
            catch (error) {
                console.error("Failed to call API:", error);
            }
        }

        for (let peer of result) {
            let peerList = document.getElementById('peer-list');
            let listElement = document.createElement('li');
            listElement.appendChild(createSpan(peer.name));
            listElement.appendChild(createSpan(peer.ip));
            for(let name of status) {
                if(name.name === peer.name)
                    listElement.appendChild(createSpan(name.status))
            }

            const configImage = document.createElement('img');
            configImage.src = '/static/icons/settings.svg';  // adjust path as needed
            configImage.alt = 'Peer icon';
            configImage.width = 20;  // optional
            configImage.height = 20;

            const deleteImage = document.createElement('img');
            deleteImage.src = '/static/icons/delete.svg';
            deleteImage.alt = 'Delete icon';
            deleteImage.width = 20;
            deleteImage.height = 20;

            listElement.appendChild(configImage);
            listElement.appendChild(deleteImage);
            peerList.appendChild(listElement);
        }
    } catch (error) {
        console.error("Failed to call API:", error);
    }
}

async function updatePeerStatus() {
    for (let peer of peers) {
        try {
            const response = await fetch("/api/peer_status", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            });
        }
        catch (error) {
            console.error("Failed to call API:", error);
        }
    }
}

makePeersTable();
setInterval(updatePeerStatus, 1000);