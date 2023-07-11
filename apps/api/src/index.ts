import express from 'express';
import mongoose from 'mongoose';
import config from '../db/config';

const app = express();
const router = express.Router();
const port = process.env.PORT || 5000;

// Connect to the MongoDB database
mongoose
  .connect(config.db.connectionString, config.db.options)
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch((error) => {
    console.error('Error connecting to MongoDB:', error);
  });

app.use('/api/users', require('./routes/users'));

// ... Other configurations and middleware

// Start the API server
app.listen(port, () => {
  console.log(`API server is running on port ${port}`);
});
