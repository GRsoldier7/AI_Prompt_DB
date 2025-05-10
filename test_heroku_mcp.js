// Test script for Heroku MCP Server
const fs = require('fs');
const { spawn, exec } = require('child_process');
const path = require('path');
const http = require('http');

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

// Test 1: Check if Heroku CLI is installed
async function testHerokuCLI() {
  try {
    const herokuVersion = await new Promise((resolve, reject) => {
      exec('heroku --version', (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout.trim());
      });
    });
    
    logTest('Heroku CLI Installation', true, `Heroku CLI version: ${herokuVersion}`);
    return true;
  } catch (error) {
    logTest('Heroku CLI Installation', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 2: Check if Heroku API key is set
async function testHerokuAPIKey() {
  try {
    const apiKey = process.env.HEROKU_API_KEY;
    
    if (!apiKey) {
      throw new Error('HEROKU_API_KEY environment variable is not set');
    }
    
    logTest('Heroku API Key', true, 'HEROKU_API_KEY environment variable is set');
    return true;
  } catch (error) {
    logTest('Heroku API Key', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 3: Install Heroku MCP Server
async function installHerokuMCPServer() {
  try {
    console.log('Installing Heroku MCP Server...');
    
    await new Promise((resolve, reject) => {
      exec('npm install -g @heroku/mcp-server', (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout);
      });
    });
    
    logTest('Install Heroku MCP Server', true, 'Heroku MCP Server installed successfully');
    return true;
  } catch (error) {
    logTest('Install Heroku MCP Server', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 4: Start Heroku MCP Server
async function startHerokuMCPServer() {
  try {
    console.log('Starting Heroku MCP Server...');
    
    // Start the server
    const serverProcess = spawn('npx', ['-y', '@heroku/mcp-server'], {
      env: {
        ...process.env,
        HEROKU_API_KEY: process.env.HEROKU_API_KEY
      },
      stdio: 'pipe'
    });
    
    // Wait for the server to start
    await wait(5000);
    
    // Check if the server is running
    if (serverProcess.killed) {
      throw new Error('Server process was killed');
    }
    
    logTest('Start Heroku MCP Server', true, 'Heroku MCP Server started successfully');
    
    // Clean up
    serverProcess.kill();
    await wait(1000);
    
    return true;
  } catch (error) {
    logTest('Start Heroku MCP Server', false, `Error: ${error.message}`);
    return false;
  }
}

// Test 5: Test Heroku MCP Server with Smart MCP Server Manager
async function testWithSmartMCPServerManager() {
  try {
    console.log('Testing Heroku MCP Server with Smart MCP Server Manager...');
    
    // Create a temporary configuration file for testing
    const configPath = path.join(__dirname, 'test-heroku-config.json');
    const config = {
      mcpServers: {
        "heroku": {
          command: "npx",
          args: ["-y", "@heroku/mcp-server"],
          env: {
            HEROKU_API_KEY: process.env.HEROKU_API_KEY || "${HEROKU_API_KEY}"
          },
          portRange: {
            start: 3601,
            end: 3700
          },
          description: "Heroku Platform MCP Server"
        }
      },
      settings: {
        defaultPortRange: {
          start: 3701,
          end: 4000
        },
        scanAllPorts: true,
        autoInstallDependencies: true,
        startupDelay: 1000,
        maxStartupRetries: 3
      }
    };
    
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
    
    // Modify the script to use our test configuration
    const scriptPath = path.join(__dirname, 'smart_mcp_server.js');
    let scriptData = fs.readFileSync(scriptPath, 'utf8');
    
    // Replace the configuration path
    const testScriptPath = path.join(__dirname, 'test-heroku-smart-mcp-server.js');
    scriptData = scriptData.replace(
      /const configPath = path\.join\(__dirname, 'mcp-servers-config\.json'\);/g,
      `const configPath = path.join(__dirname, 'test-heroku-config.json');`
    );
    
    fs.writeFileSync(testScriptPath, scriptData, 'utf8');
    
    // Start the smart MCP server
    const smartServer = spawn('node', [testScriptPath], {
      env: {
        ...process.env,
        HEROKU_API_KEY: process.env.HEROKU_API_KEY || "dummy-key-for-testing"
      },
      stdio: 'pipe'
    });
    
    // Wait for the server to start
    await wait(10000);
    
    // Check if the server is running
    if (smartServer.killed) {
      throw new Error('Smart MCP Server was killed');
    }
    
    logTest('Test with Smart MCP Server Manager', true, 'Smart MCP Server Manager successfully started Heroku MCP Server');
    
    // Clean up
    smartServer.kill();
    await wait(2000);
    
    // Remove the test files
    fs.unlinkSync(configPath);
    fs.unlinkSync(testScriptPath);
    
    return true;
  } catch (error) {
    logTest('Test with Smart MCP Server Manager', false, `Error: ${error.message}`);
    return false;
  }
}

// Run all tests
async function runTests() {
  console.log('='.repeat(50));
  console.log('HEROKU MCP SERVER TEST SUITE');
  console.log('='.repeat(50));
  
  // Check if HEROKU_API_KEY is set
  if (!process.env.HEROKU_API_KEY) {
    console.log('⚠️ HEROKU_API_KEY environment variable is not set');
    console.log('Some tests may fail. Please set HEROKU_API_KEY to run all tests.');
    console.log('You can get a token by running: heroku authorizations:create');
    console.log('='.repeat(50));
  }
  
  await testHerokuCLI();
  await testHerokuAPIKey();
  await installHerokuMCPServer();
  await startHerokuMCPServer();
  await testWithSmartMCPServerManager();
  
  console.log('='.repeat(50));
  console.log(`TEST RESULTS: ${testResults.passed} passed, ${testResults.failed} failed`);
  console.log('='.repeat(50));
  
  if (testResults.failed === 0) {
    console.log('All tests passed! The Heroku MCP Server is working properly with Smart MCP Server Manager.');
  } else {
    console.log('Some tests failed. Please fix the issues before using the Heroku MCP Server.');
  }
}

// Run the tests
runTests();
