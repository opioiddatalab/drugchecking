module.exports = {
    db: {
      connectionString: `mongodb+srv://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@cluster0.tejymzw.mongodb.net/?retryWrites=true&w=majority`, 
      options: {
        useUnifiedTopology: true,
      },
    },
    secret: 'j8I04r6MQc'
  };
