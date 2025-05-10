// Test script for Smart MCP Server Manager
const fs = require('fs');
const { spawn, exec } = require('child_process');
const path = require('path');
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

// Test 1: Check if Node.js is installed
async function testNodeInstallation() {
  try {
    const nodeVersion = await new Promise((resolve, reject) => {
      exec('node -v', (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout.trim());
      });
    });
    
    logTest('Node.js Installation', true, `Node.js version: ${nodeVersion}`);
    return true;
  } catch (error) {
    logTest('Node.js Installation', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 2: Check if required packages are installed
async function testRequiredPackages() {
  try {
    await new Promise((resolve, reject) => {
      exec('npm list dotenv', (error, stdout, stderr) => {
        if (error && error.code !== 0) reject(error);
        else resolve(stdout);
      });
    });
    
    logTest('Required Packages', true, 'dotenv package is installed');
    return true;
  } catch (error) {
    logTest('Required Packages', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 3: Check if configuration file exists and is valid
async function testConfigFile() {
  try {
    const configPath = path.join(__dirname, 'mcp-servers-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    // Check if config has required structure
    if (!config.mcpServers) {
      throw new Error('Configuration file is missing mcpServers property');
    }
    
    if (!config.settings) {
      throw new Error('Configuration file is missing settings property');
    }
    
    // Check if at least one server is configured
    const serverCount = Object.keys(config.mcpServers).length;
    if (serverCount === 0) {
      throw new Error('No MCP servers configured');
    }
    
    logTest('Configuration File', true, `Found ${serverCount} configured MCP servers`);
    return true;
  } catch (error) {
    logTest('Configuration File', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 4: Check if port scanning works
async function testPortScanning() {
  try {
    // Create a server on a random port
    const server = net.createServer();
    const port = await new Promise((resolve) => {
      server.listen(0, () => {
        resolve(server.address().port);
      });
    });
    
    // Check if port is in use
    const isInUse = await new Promise((resolve) => {
      const testSocket = new net.Socket();
      testSocket.setTimeout(1000);
      testSocket.on('connect', () => {
        testSocket.destroy();
        resolve(true);
      });
      testSocket.on('timeout', () => {
        testSocket.destroy();
        resolve(false);
      });
      testSocket.on('error', () => {
        testSocket.destroy();
        resolve(false);
      });
      testSocket.connect(port);
    });
    
    // Close the server
    await new Promise((resolve) => {
      server.close(() => resolve());
    });
    
    if (isInUse) {
      logTest('Port Scanning', true, `Successfully detected port ${port} as in use`);
      return true;
    } else {
      logTest('Port Scanning', false, `Failed to detect port ${port} as in use`);
      return false;
    }
  } catch (error) {
    logTest('Port Scanning', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 5: Check if smart_mcp_server.js exists and is valid
async function testServerScript() {
  try {
    const scriptPath = path.join(__dirname, 'smart_mcp_server.js');
    const scriptData = fs.readFileSync(scriptPath, 'utf8');
    
    // Check if script contains key functions
    if (!scriptData.includes('function startMCPServer')) {
      throw new Error('Script is missing startMCPServer function');
    }
    
    if (!scriptData.includes('function stopAllServers')) {
      throw new Error('Script is missing stopAllServers function');
    }
    
    if (!scriptData.includes('function scanAllPorts')) {
      throw new Error('Script is missing scanAllPorts function');
    }
    
    logTest('Server Script', true, 'Script contains all required functions');
    return true;
  } catch (error) {
    logTest('Server Script', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 6: Check if add_mcp_server.js exists and is valid
async function testAddServerScript() {
  try {
    const scriptPath = path.join(__dirname, 'add_mcp_server.js');
    const scriptData = fs.readFileSync(scriptPath, 'utf8');
    
    // Check if script contains key functions
    if (!scriptData.includes('function addMCPServer')) {
      throw new Error('Script is missing addMCPServer function');
    }
    
    logTest('Add Server Script', true, 'Script contains all required functions');
    return true;
  } catch (error) {
    logTest('Add Server Script', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 7: Check if batch files exist
async function testBatchFiles() {
  try {
    const files = [
      'start_smart_mcp.bat',
      'add_mcp_server.bat'
    ];
    
    const missingFiles = [];
    
    for (const file of files) {
      const filePath = path.join(__dirname, file);
      if (!fs.existsSync(filePath)) {
        missingFiles.push(file);
      }
    }
    
    if (missingFiles.length === 0) {
      logTest('Batch Files', true, 'All batch files exist');
      return true;
    } else {
      throw new Error(`Missing batch files: ${missingFiles.join(', ')}`);
    }
  } catch (error) {
    logTest('Batch Files', false, `Error: ${error.message}`);
    return false;
  }
}

// Run all tests
async function runTests() {
  console.log('='.repeat(50));
  console.log('SMART MCP SERVER MANAGER TEST SUITE');
  console.log('='.repeat(50));
  
  await testNodeInstallation();
  await testRequiredPackages();
  await testConfigFile();
  await testPortScanning();
  await testServerScript();
  await testAddServerScript();
  await testBatchFiles();
  
  console.log('='.repeat(50));
  console.log(`TEST RESULTS: ${testResults.passed} passed, ${testResults.failed} failed`);
  console.log('='.repeat(50));
  
  if (testResults.failed === 0) {
    console.log('All tests passed! The Smart MCP Server Manager is ready to use.');
  } else {
    console.log('Some tests failed. Please fix the issues before using the Smart MCP Server Manager.');
  }
}

// Run the tests
runTests();
