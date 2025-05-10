// Advanced MCP Server Manager with Port Scanning
const fs = require('fs');
const { spawn, exec } = require('child_process');
const dotenv = require('dotenv');
const path = require('path');
const net = require('net');

// Load environment variables
dotenv.config();

// Default port ranges will be loaded from config file
let DEFAULT_PORT_RANGES = {
  'default': { start: 3601, end: 4000 } // Default fallback
};

// Store running server information
const runningServers = {};

// Function to check if a port is in use
function isPortInUse(port) {
  return new Promise((resolve) => {
    const server = net.createServer()
      .once('error', () => resolve(true))
      .once('listening', () => {
        server.close();
        resolve(false);
      })
      .listen(port);
  });
}

// Function to find an available port in a range
async function findAvailablePort(startPort, endPort) {
  console.log(`Scanning for available ports between ${startPort} and ${endPort}...`);
  for (let port = startPort; port <= endPort; port++) {
    const inUse = await isPortInUse(port);
    if (!inUse) {
      console.log(`Found available port: ${port}`);
      return port;
    }
  }
  throw new Error(`No available ports found in range ${startPort}-${endPort}`);
}

// Function to scan all ports and create a map of used ports
async function scanAllPorts() {
  console.log('Performing comprehensive port scan...');

  // Execute netstat to get all listening ports
  return new Promise((resolve, reject) => {
    exec('netstat -ano | findstr LISTENING', (error, stdout, stderr) => {
      if (error && error.code !== 1) {
        console.error(`Error scanning ports: ${error.message}`);
        reject(error);
        return;
      }

      const usedPorts = new Set();

      // Parse the output to extract port numbers
      const lines = stdout.split('\n');
      for (const line of lines) {
        const parts = line.trim().split(/\s+/);
        if (parts.length >= 2) {
          const addressPart = parts[1];
          const portMatch = addressPart.match(/:(\d+)$/);
          if (portMatch && portMatch[1]) {
            usedPorts.add(parseInt(portMatch[1], 10));
          }
        }
      }

      console.log(`Found ${usedPorts.size} ports in use`);
      resolve(usedPorts);
    });
  });
}

// Function to start an MCP server with a specific port
async function startMCPServer(serverName, command, args, env = {}, usedPorts) {
  console.log(`Starting ${serverName} MCP server...`);

  // Determine port range for this server
  const portRange = DEFAULT_PORT_RANGES[serverName] || DEFAULT_PORT_RANGES.default;

  // Find an available port
  const port = await findAvailablePort(portRange.start, portRange.end);

  // Prepare environment variables
  const processEnv = { ...process.env, PORT: port.toString() };

  // Replace environment variable placeholders with actual values
  for (const [key, value] of Object.entries(env)) {
    if (typeof value === 'string' && value.startsWith('${') && value.endsWith('}')) {
      const envVarName = value.slice(2, -1);
      processEnv[key] = process.env[envVarName] || '';
      if (!processEnv[key]) {
        console.warn(`Warning: Environment variable ${envVarName} is not set for ${serverName}`);
      }
    } else {
      processEnv[key] = value;
    }
  }

  // Add port to args if needed
  const finalArgs = [...args];
  if (!args.some(arg => arg.includes('--port') || arg.includes('-p'))) {
    finalArgs.push('--port', port.toString());
  }

  // Start the MCP server process
  const serverProcess = spawn(command, finalArgs, {
    env: processEnv,
    stdio: 'inherit'
  });

  // Store server information
  runningServers[serverName] = {
    process: serverProcess,
    port: port,
    startTime: new Date()
  };

  // Handle process events
  serverProcess.on('error', (error) => {
    console.error(`Error starting ${serverName} server:`, error);
    delete runningServers[serverName];
  });

  serverProcess.on('close', (code) => {
    console.log(`${serverName} server exited with code ${code}`);
    delete runningServers[serverName];
  });

  console.log(`${serverName} server started on port ${port}`);
  return serverProcess;
}

// Function to stop all running servers
function stopAllServers() {
  console.log('Shutting down all MCP servers...');

  for (const [serverName, server] of Object.entries(runningServers)) {
    if (server.process && !server.process.killed) {
      console.log(`Stopping ${serverName} server on port ${server.port}...`);
      server.process.kill();
    }
  }

  console.log('All servers stopped');
}

// Function to install dependencies if needed
async function installDependencies(dependencies) {
  if (!dependencies) return;

  // Install npm dependencies
  if (dependencies.npm) {
    for (const pkg of dependencies.npm) {
      console.log(`Installing npm package: ${pkg}...`);
      await new Promise((resolve, reject) => {
        exec(`npm install ${pkg}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`Error installing ${pkg}: ${error.message}`);
            reject(error);
            return;
          }
          console.log(`Successfully installed ${pkg}`);
          resolve();
        });
      });
    }
  }

  // Install pip dependencies
  if (dependencies.pip) {
    for (const pkg of dependencies.pip) {
      console.log(`Installing pip package: ${pkg}...`);
      await new Promise((resolve, reject) => {
        exec(`pip install ${pkg}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`Error installing ${pkg}: ${error.message}`);
            reject(error);
            return;
          }
          console.log(`Successfully installed ${pkg}`);
          resolve();
        });
      });
    }
  }
}

// Main function to start all servers
async function startAllServers() {
  try {
    // Read the MCP configuration
    const configPath = path.join(__dirname, 'mcp-servers-config.json');
    console.log(`Loading configuration from ${configPath}`);

    let configData, config;
    try {
      configData = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(configData);
    } catch (err) {
      console.warn(`Could not load ${configPath}, falling back to mcp-config.json`);
      const fallbackPath = path.join(__dirname, 'mcp-config.json');
      configData = fs.readFileSync(fallbackPath, 'utf8');
      config = JSON.parse(configData);
    }

    // Load settings
    const settings = config.settings || {};
    const scanAllPortsEnabled = settings.scanAllPorts !== false;
    const autoInstallDeps = settings.autoInstallDependencies !== false;
    const startupDelay = settings.startupDelay || 1000;
    const maxRetries = settings.maxStartupRetries || 3;

    // Update default port ranges from config
    if (settings.defaultPortRange) {
      DEFAULT_PORT_RANGES.default = settings.defaultPortRange;
    }

    // Load port ranges from server configs
    for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
      if (serverConfig.portRange) {
        DEFAULT_PORT_RANGES[serverName] = serverConfig.portRange;
      }
    }

    // Scan for used ports if enabled
    const usedPorts = scanAllPortsEnabled ? await scanAllPorts() : new Set();

    // Install dependencies if needed
    if (autoInstallDeps) {
      for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
        if (serverConfig.dependencies) {
          console.log(`Checking dependencies for ${serverName}...`);
          await installDependencies(serverConfig.dependencies);
        }
      }
    }

    // Start each server
    const startPromises = [];
    for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
      const { command, args, env } = serverConfig;

      // Add a small delay between starting servers to avoid port conflicts
      await new Promise(resolve => setTimeout(resolve, startupDelay));

      startPromises.push(startMCPServer(serverName, command, args, env, usedPorts));
    }

    await Promise.all(startPromises);

    console.log('\n='.repeat(25));
    console.log('All MCP servers started successfully');
    console.log('='.repeat(25));
    console.log('Server Status:');
    for (const [name, server] of Object.entries(runningServers)) {
      const uptime = Math.round((new Date() - server.startTime) / 1000);
      console.log(`- ${name}: running on port ${server.port} (up for ${uptime}s)`);
    }
    console.log('='.repeat(25));
    console.log('Press Ctrl+C to stop all servers');
    console.log('='.repeat(25));

    // Handle process termination
    process.on('SIGINT', () => {
      stopAllServers();
      process.exit(0);
    });

    // Also handle Windows CTRL+C
    if (process.platform === 'win32') {
      const rl = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
      });

      rl.on('SIGINT', () => {
        process.emit('SIGINT');
      });
    }

  } catch (error) {
    console.error('Error starting MCP servers:', error);
    stopAllServers();
    process.exit(1);
  }
}

// Run the function
console.log('='.repeat(50));
console.log('SMART MCP SERVER MANAGER');
console.log('='.repeat(50));
console.log('Press Ctrl+C to stop all servers');
console.log('='.repeat(50));
startAllServers();
