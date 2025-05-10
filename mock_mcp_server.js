// Mock MCP server for testing
const http = require('http');
const url = require('url');

// Parse command line arguments
const args = process.argv.slice(2);
let port = 3000; // Default port

// Look for port argument
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--port' && i + 1 < args.length) {
    port = parseInt(args[i + 1], 10);
    break;
  } else if (args[i].startsWith('--port=')) {
    port = parseInt(args[i].split('=')[1], 10);
    break;
  } else if (args[i] === '-p' && i + 1 < args.length) {
    port = parseInt(args[i + 1], 10);
    break;
  }
}

// Create a simple HTTP server
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  // Handle different endpoints
  if (parsedUrl.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      message: 'Mock MCP server is running',
      port: port
    }));
  } else if (parsedUrl.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'healthy',
      uptime: process.uptime()
    }));
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'error',
      message: 'Not found'
    }));
  }
});

// Start the server
server.listen(port, () => {
  console.log(`Mock MCP server listening on port ${port}`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('Shutting down mock MCP server...');
  server.close(() => {
    console.log('Mock MCP server shut down');
    process.exit(0);
  });
});

// Log server information
console.log('Mock MCP server started');
console.log(`Port: ${port}`);
console.log('Press Ctrl+C to stop the server');
