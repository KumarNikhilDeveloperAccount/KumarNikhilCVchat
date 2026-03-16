import { createServer } from "node:http";

const port = Number(process.env.PORT || 8081);
const clients = new Set();

function sendEvent(client, event, data) {
  client.write(`event: ${event}\n`);
  client.write(`data: ${JSON.stringify(data)}\n\n`);
}

const server = createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", service: "events" }));
    return;
  }

  if (req.method === "GET" && req.url === "/stream") {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "Access-Control-Allow-Origin": "*"
    });
    res.write("\n");
    clients.add(res);
    sendEvent(res, "connected", { status: "ready" });
    req.on("close", () => clients.delete(res));
    return;
  }

  if (req.method === "POST" && req.url === "/publish") {
    const chunks = [];
    for await (const chunk of req) {
      chunks.push(chunk);
    }
    const payload = JSON.parse(Buffer.concat(chunks).toString() || "{}");
    for (const client of clients) {
      sendEvent(client, payload.event || "message", payload.data || {});
    }
    res.writeHead(202, { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" });
    res.end(JSON.stringify({ accepted: true, clients: clients.size }));
    return;
  }

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    });
    res.end();
    return;
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Not found" }));
});

server.listen(port, () => {
  console.log(`events listening on ${port}`);
});
