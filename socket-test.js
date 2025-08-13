// ===========================
// Render WebSocket Test Script
// ===========================

const orderId = "BO4014714"; // Replace with your order ID
const baseUrl = "wss://bistropulse-backend.onrender.com/ws/orders/";

let socket;
let reconnectInterval = 5000; // 5 seconds
let manuallyClosed = false;

function connectWS() {
    socket = new WebSocket(`${baseUrl}${orderId}/`);

    socket.onopen = () => {
        console.log(`✅ Connected to WSS for order ${orderId}`);
        // Example: send a test message to server
        socket.send(JSON.stringify({ test: "Hello server!" }));
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log("📩 Message from server:", data);
        } catch (err) {
            console.log("📩 Raw message from server:", event.data);
        }
    };

    socket.onclose = (event) => {
        console.log(`❌ WebSocket closed (code: ${event.code}, reason: ${event.reason})`);
        if (!manuallyClosed) {
            console.log(`🔄 Reconnecting in ${reconnectInterval / 1000}s...`);
            setTimeout(connectWS, reconnectInterval);
        }
    };

    socket.onerror = (error) => {
        console.error("⚠️ WebSocket error:", error);
    };
}

// Call this to start the connection
connectWS();

// Optional: send a message manually
function sendMessage(msg) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(msg));
        console.log("📤 Sent:", msg);
    } else {
        console.log("⚠️ Socket not open. Try again later.");
    }
}

// Optional: close socket manually
function closeSocket() {
    manuallyClosed = true;
    if (socket) socket.close();
}
