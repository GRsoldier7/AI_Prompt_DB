// Comprehensive test for Smart MCP Server Manager with mock server
const fs = require('fs');
const { spawn, exec } = require('child_process');
const path = require('path');
const http = require('http');
const net = require('net');

// Test results
const testResults = {
  passed: 0,
  failed: 0,
  tests: []
};

// Helper function to log test results
function logTest(name, passed, message) {
  const result = {
    name,
    passed,
    message
  };
  
  testResults.tests.push(result);
  
  if (passed) {
    testResults.passed++;
    console.log(`✅ PASS: ${name}`);
    if (message) console.log(`   ${message}`);
  } else {
    testResults.failed++;
    console.log(`❌ FAIL: ${name}`);
    console.log(`   ${message}`);
  }
  
  console.log(''); // Empty line for readability
}

// Helper function to wait for a specific time
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Helper function to check if a port is in use
async function isPortInUse(port) {
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

// Helper function to make an HTTP request
async function makeRequest(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          resolve({
            statusCode: res.statusCode,
            data: JSON.parse(data)
          });
        } catch (error) {
          reject(error);
        }
      });
    }).on('error', (error) => {
      reject(error);
    });
  });
}

// Test 1: Create a temporary configuration file for testing
async function createTestConfig() {
  try {
    const configPath = path.join(__dirname, 'test-mcp-config.json');
    const config = {
      mcpServers: {
        "mock-server": {
          command: "node",
          args: ["mock_mcp_server.js"],
          portRange: {
            start: 3000,
            end: 3100
          },
          description: "Mock MCP server for testing"
        }
      },
      settings: {
        defaultPortRange: {
          start: 3601,
          end: 4000
        },
        scanAllPorts: true,
        autoInstallDependencies: true,
        startupDelay: 1000,
        maxStartupRetries: 3
      }
    };
    
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
    logTest('Create Test Config', true, `Created test configuration at ${configPath}`);
    return true;
  } catch (error) {
    logTest('Create Test Config', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 2: Start a mock MCP server directly
async function startMockServer() {
  try {
    // Find an available port
    let port = 3000;
    while (await isPortInUse(port)) {
      port++;
      if (port > 3100) {
        throw new Error('No available ports found in range 3000-3100');
      }
    }
    
    // Start the mock server
    const mockServer = spawn('node', ['mock_mcp_server.js', '--port', port.toString()], {
      stdio: 'pipe'
    });
    
    // Wait for the server to start
    await wait(2000);
    
    // Check if the server is running
    try {
      const response = await makeRequest(`http://localhost:${port}`);
      if (response.statusCode === 200 && response.data.status === 'ok') {
        logTest('Start Mock Server', true, `Mock server started on port ${port}`);
        
        // Clean up
        mockServer.kill();
        await wait(1000);
        
        return true;
      } else {
        throw new Error(`Unexpected response: ${JSON.stringify(response)}`);
      }
    } catch (error) {
      mockServer.kill();
      throw error;
    }
  } catch (error) {
    logTest('Start Mock Server', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 3: Test the smart_mcp_server.js script with the mock server
async function testSmartMCPServer() {
  try {
    // Modify the script to use our test configuration
    const scriptPath = path.join(__dirname, 'smart_mcp_server.js');
    let scriptData = fs.readFileSync(scriptPath, 'utf8');
    
    // Replace the configuration path
    scriptData = scriptData.replace(
      /const configPath = path\.join\(__dirname, 'mcp-servers-config\.json'\);/g,
      "const configPath = path.join(__dirname, 'test-mcp-config.json');"
    );
    
    // Save the modified script
    const testScriptPath = path.join(__dirname, 'test-smart-mcp-server.js');
    fs.writeFileSync(testScriptPath, scriptData, 'utf8');
    
    // Start the smart MCP server
    const smartServer = spawn('node', [testScriptPath], {
      stdio: 'pipe'
    });
    
    // Wait for the server to start
    await wait(5000);
    
    // Check if the mock server is running
    let success = false;
    for (let port = 3000; port <= 3100; port++) {
      try {
        const response = await makeRequest(`http://localhost:${port}`);
        if (response.statusCode === 200 && response.data.status === 'ok') {
          logTest('Test Smart MCP Server', true, `Smart MCP Server successfully started mock server on port ${port}`);
          success = true;
          break;
        }
      } catch (error) {
        // Ignore errors, just try the next port
      }
    }
    
    if (!success) {
      throw new Error('Could not connect to mock server started by Smart MCP Server');
    }
    
    // Clean up
    smartServer.kill();
    await wait(2000);
    
    // Remove the test script
    fs.unlinkSync(testScriptPath);
    
    return true;
  } catch (error) {
    logTest('Test Smart MCP Server', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 4: Clean up test files
async function cleanUp() {
  try {
    const configPath = path.join(__dirname, 'test-mcp-config.json');
    if (fs.existsSync(configPath)) {
      fs.unlinkSync(configPath);
    }
    
    const testScriptPath = path.join(__dirname, 'test-smart-mcp-server.js');
    if (fs.existsSync(testScriptPath)) {
      fs.unlinkSync(testScriptPath);
    }
    
    logTest('Clean Up', true, 'Removed all test files');
    return true;
  } catch (error) {
    logTest('Clean Up', false, `Error: ${error.message}`);
    return false;
  }
}

// Run all tests
async function runTests() {
  console.log('='.repeat(50));
  console.log('SMART MCP SERVER MANAGER COMPREHENSIVE TEST');
  console.log('='.repeat(50));
  
  await createTestConfig();
  await startMockServer();
  await testSmartMCPServer();
  await cleanUp();
  
  console.log('='.repeat(50));
  console.log(`TEST RESULTS: ${testResults.passed} passed, ${testResults.failed} failed`);
  console.log('='.repeat(50));
  
  if (testResults.failed === 0) {
    console.log('All tests passed! The Smart MCP Server Manager is working properly.');
  } else {
    console.log('Some tests failed. Please fix the issues before using the Smart MCP Server Manager.');
  }
}

// Run the tests
runTests();
