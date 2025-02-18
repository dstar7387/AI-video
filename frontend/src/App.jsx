
import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [images, setImages] = useState([]);
  const [message, setMessage] = useState('');
  const fileInputRef = useRef(null);
  const speechInputRef = useRef(null);
  const backgroundInputRef = useRef(null);

  const handleImageUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const files = fileInputRef.current.files;
    
    for (let file of files) {
      formData.append('file', file);
    }

    try {
      await axios.post('http://localhost:5000/upload', formData);
      const response = await axios.get('http://localhost:5000/images');
      setImages(response.data);
    } catch (error) {
      setMessage('Error uploading images');
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('speech', speechInputRef.current.files[0]);
    formData.append('background', backgroundInputRef.current.files[0]);

    try {
      const response = await axios.post('http://localhost:5000/generate', formData);
      window.location.href = '/result';
    } catch (error) {
      setMessage('Error generating slideshow');
    }
  };

  const handleDelete = async (image) => {
    try {
      await axios.get(`http://localhost:5000/delete/${image}`);
      setImages(images.filter(img => img !== image));
    } catch (error) {
      setMessage('Error deleting image');
    }
  };

  return (
    <div>
      <h1>Images to Slideshow Video Generator</h1>
      
      <h2>Upload Images</h2>
      <form onSubmit={handleImageUpload}>
        <input type="file" multiple ref={fileInputRef} />
        <button type="submit">Upload</button>
      </form>

      <div className="image-list">
        {images.map((image, index) => (
          <div key={index} className="image-item">
            <img src={`http://localhost:5000/myimg/${image}`} alt={image} height="100" />
            <button onClick={() => handleDelete(image)}>Delete</button>
          </div>
        ))}
      </div>

      <h2>Upload MP3 Files</h2>
      <form onSubmit={handleGenerate}>
        <div>
          <label htmlFor="speech">Upload Speech MP3:</label>
          <input type="file" id="speech" accept=".mp3" ref={speechInputRef} required />
        </div>
        
        <div>
          <label htmlFor="background">Upload Background MP3:</label>
          <input type="file" id="background" accept=".mp3" ref={backgroundInputRef} required />
        </div>

        <button type="submit">Generate Slideshow</button>
      </form>

      {message && <p className="message">{message}</p>}
      
      <footer className="footer">
        <p className="footer-text">
          © Created by <a href="https://about.me/mohaimenulislamshawon/" target="_blank" className="footer-link">Shawon</a>
        </p>
      </footer>
    </div>
  );
}

export default App;
