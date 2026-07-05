(function () {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socketUrl = `${protocol}://${window.location.host}/ws/alerts`;

    let socket = null;
    let reconnectDelay = 1000;
    const maxReconnectDelay = 15000;

    function showNotification(notification) {
        const containerId = "live-alert-container";

        let container = document.getElementById(containerId);

        if (!container) {
            container = document.createElement("div");
            container.id = containerId;
            container.style.position = "fixed";
            container.style.top = "20px";
            container.style.right = "20px";
            container.style.zIndex = "9999";
            container.style.maxWidth = "360px";
            document.body.appendChild(container);
        }

        const alert = document.createElement("div");

        alert.style.background = "#ffffff";
        alert.style.border = "1px solid #d1d5db";
        alert.style.borderRadius = "10px";
        alert.style.padding = "14px";
        alert.style.marginBottom = "10px";
        alert.style.boxShadow = "0 8px 20px rgba(0,0,0,0.15)";
        alert.style.fontFamily = "Arial, sans-serif";

        const title = document.createElement("strong");
        title.textContent = notification.title || "New notification";

        const message = document.createElement("div");
        message.textContent = notification.message || "";
        message.style.marginTop = "6px";

        alert.appendChild(title);
        alert.appendChild(message);

        if (
            notification.type === "new_ticket" &&
            notification.data &&
            notification.data.ticket_id
        ) {
            alert.style.cursor = "pointer";

            alert.addEventListener("click", function () {
                window.location.href =
                    `/ticket/${notification.data.ticket_id}`;
            });
        }

        container.appendChild(alert);

        setTimeout(function () {
            alert.remove();
        }, 8000);
    }

    function connect() {
        socket = new WebSocket(socketUrl);

        socket.onopen = function () {
            reconnectDelay = 1000;

            setInterval(function () {
                if (socket.readyState === WebSocket.OPEN) {
                    socket.send("ping");
                }
            }, 25000);
        };

        socket.onmessage = function (event) {
            try {
                const notification = JSON.parse(event.data);
                showNotification(notification);
            } catch (error) {
                console.error("Invalid live notification:", error);
            }
        };

        socket.onclose = function () {
            setTimeout(connect, reconnectDelay);
            reconnectDelay = Math.min(
                reconnectDelay * 2,
                maxReconnectDelay
            );
        };

        socket.onerror = function () {
            socket.close();
        };
    }

    connect();
})();