// Script to test all MCP servers
const fs = require('fs');
const { spawn } = require('child_process');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

// Function to test a single MCP server
async function testServer(serverName, serverConfig) {
  const { command, args, env = {} } = serverConfig;
  
  console.log(`\n🔍 Testing ${serverName} MCP server...`);
  
  // Prepare environment variables
  const processEnv = { ...process.env };
  
  // Replace environment variable placeholders with actual values
  for (const [key, value] of Object.entries(env)) {
    if (typeof value === 'string' && value.startsWith('${') && value.endsWith('}')) {
      const envVarName = value.slice(2, -1);
      processEnv[key] = process.env[envVarName] || '';
      if (!processEnv[key]) {
        console.warn(`⚠️ Warning: Environment variable ${envVarName} is not set for ${serverName}`);
      }
    } else {
      processEnv[key] = value;
    }
  }
  
  return new Promise((resolve) => {
    // Start the MCP server process
    const serverProcess = spawn(command, args, { 
      env: processEnv,
      stdio: 'pipe'
    });
    
    let output = '';
    let errorOutput = '';
    let success = false;
    
    // Handle process output
    serverProcess.stdout.on('data', (data) => {
      const dataStr = data.toString();
      output += dataStr;
      console.log(`${serverName} output: ${dataStr.trim()}`);
      
      // Check for success indicators in the output
      if (dataStr.includes('Server started') || 
          dataStr.includes('listening') || 
          dataStr.includes('ready') ||
          dataStr.includes('MCP server started')) {
        success = true;
      }
    });
    
    serverProcess.stderr.on('data', (data) => {
      const dataStr = data.toString();
      errorOutput += dataStr;
      console.error(`${serverName} error: ${dataStr.trim()}`);
      
      // Some servers output to stderr even when successful
      if (dataStr.includes('Server started') || 
          dataStr.includes('listening') || 
          dataStr.includes('ready') ||
          dataStr.includes('MCP server started')) {
        success = true;
      }
    });
    
    // Set a timeout to check the server status
    setTimeout(() => {
      if (!serverProcess.killed) {
        console.log(`${serverName} server is running`);
        
        // If we haven't detected success but the server is still running, consider it a success
        if (!success && !errorOutput.includes('Error') && !errorOutput.includes('error')) {
          success = true;
        }
        
        // Kill the process
        serverProcess.kill();
        
        if (success) {
          console.log(`✅ ${serverName} server test PASSED`);
          resolve(true);
        } else {
          console.error(`❌ ${serverName} server test FAILED`);
          console.error(`Output: ${output}`);
          console.error(`Error: ${errorOutput}`);
          resolve(false);
        }
      } else {
        console.error(`❌ ${serverName} server test FAILED - process terminated unexpectedly`);
        resolve(false);
      }
    }, 10000); // Wait 10 seconds
    
    // Handle process exit
    serverProcess.on('error', (error) => {
      console.error(`Error starting ${serverName} server:`, error);
      resolve(false);
    });
    
    serverProcess.on('close', (code) => {
      if (code !== 0 && code !== null) {
        console.error(`${serverName} server exited with code ${code}`);
        resolve(false);
      }
    });
  });
}

// Main function to test all servers
async function testAllServers() {
  try {
    // Read the MCP configuration
    const configPath = path.join(__dirname, 'mcp-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    console.log('🚀 Starting tests for all MCP servers...\n');
    
    const results = {};
    
    // Test each server sequentially
    for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
      results[serverName] = await testServer(serverName, serverConfig);
      
      // Add a small delay between server tests
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Print summary
    console.log('\n📊 Test Results Summary:');
    console.log('=======================');
    
    let allPassed = true;
    
    for (const [serverName, success] of Object.entries(results)) {
      if (success) {
        console.log(`✅ ${serverName}: PASSED`);
      } else {
        console.log(`❌ ${serverName}: FAILED`);
        allPassed = false;
      }
    }
    
    console.log('\n');
    
    if (allPassed) {
      console.log('🎉 All MCP servers are working correctly!');
    } else {
      console.error('⚠️ Some MCP servers failed the test. Please check the logs above for details.');
    }
    
  } catch (error) {
    console.error('Error testing MCP servers:', error);
  }
}

// Run the tests
testAllServers();
