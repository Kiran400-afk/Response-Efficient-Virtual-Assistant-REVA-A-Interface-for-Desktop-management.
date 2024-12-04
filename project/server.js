import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

const app = express();
const server = createServer(app);
const io = new Server(server);

// Serve static files
app.use(express.static(join(__dirname, 'public')));

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('command', async (command) => {
    try {
      // Process voice command
      const response = await processCommand(command);
      socket.emit('response', response);
    } catch (error) {
      console.error('Error processing command:', error);
      socket.emit('error', 'Error processing command');
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

async function processCommand(command) {
  // Basic command processing
  const cmd = command.toLowerCase();
  if (cmd.includes('hello')) {
    return 'Hello! How can I help you today?';
  } else if (cmd.includes('goodbye')) {
    return 'Goodbye! Have a great day!';
  }
  return `I heard: ${command}`;
}

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});