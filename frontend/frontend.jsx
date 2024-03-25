import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [userQuestion, setUserQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('pdf_files', selectedFiles[i]);
    }

    try {
      await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setError('');
    } catch (err) {
      setError('Error uploading PDF files.');
    }
  };

  const handleQuery = async () => {
    try {
      const { data } = await axios.post('http://127.0.0.1:8000/query/', {
        user_question: userQuestion,
      });
      setResponse(data.response);
      setError('');
    } catch (err) {
      setError('Error querying document.');
    }
  };

  return (
    <div>
      <h1>Document Query Support</h1>
      <div>
        <input type="file" onChange={handleFileChange} multiple />
        <button onClick={handleUpload}>Upload PDF</button>
      </div>
      <div>
        <input
          type="text"
          placeholder="Enter your question"
          value={userQuestion}
          onChange={(e) => setUserQuestion(e.target.value)}
        />
        <button onClick={handleQuery}>Query</button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {response && <p>{response}</p>}
    </div>
  );
};

export default App;
