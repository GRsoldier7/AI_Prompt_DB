// Script to install all necessary dependencies for MCP servers
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Installing dependencies for MCP servers...');

// Install dotenv for environment variable management
try {
  console.log('Installing dotenv...');
  execSync('npm install dotenv', { stdio: 'inherit' });
} catch (error) {
  console.error('Error installing dotenv:', error);
  process.exit(1);
}

// Read the MCP configuration
try {
  const configPath = path.join(__dirname, 'mcp-config.json');
  const configData = fs.readFileSync(configPath, 'utf8');
  const config = JSON.parse(configData);
  
  // Install each MCP server package
  for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
    if (serverConfig.command === 'npx' && serverConfig.args && serverConfig.args.length > 0) {
      const packageName = serverConfig.args.find(arg => !arg.startsWith('-'));
      
      if (packageName) {
        console.log(`Installing ${packageName}...`);
        try {
          execSync(`npm install -g ${packageName}`, { stdio: 'inherit' });
          console.log(`Successfully installed ${packageName}`);
        } catch (error) {
          console.error(`Error installing ${packageName}:`, error);
        }
      }
    }
  }
  
  console.log('All dependencies installed successfully!');
} catch (error) {
  console.error('Error reading configuration or installing dependencies:', error);
  process.exit(1);
}
