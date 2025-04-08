import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// Configuración del backend
const BACKEND_URL = 'http://127.0.0.1:3000';

// Configuración de axios
axios.defaults.timeout = 5000; // 5 segundos de timeout
axios.defaults.headers.common['Content-Type'] = 'multipart/form-data';

function App() {
  const [file, setFile] = useState(null);
  const [date, setDate] = useState('');
  const [email, setEmail] = useState('');
  const [fileName, setFileName] = useState('');
  const [backendResponse, setBackendResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleDateChange = (e) => {
    setDate(e.target.value);
    setError(null);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validaciones
    if (!file) {
      setError('Por favor selecciona un archivo');
      setLoading(false);
      return;
    }
    if (!date) {
      setError('Por favor selecciona una fecha');
      setLoading(false);
      return;
    }
    if (!email) {
      setError('Por favor ingresa un correo electrónico');
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('date', date);
    formData.append('email', email);

    try {
      console.log('Intentando conectar con:', `${BACKEND_URL}/upload`);
      const response = await axios.post(`${BACKEND_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        validateStatus: function (status) {
          return status >= 200 && status < 500; // Acepta cualquier estado entre 200-499
        }
      });
      
      if (response.status === 200) {
        setFileName(response.data.fileName);
        setBackendResponse(response.data);
        alert('¡Archivo procesado exitosamente!');
      } else {
        throw new Error(`Error del servidor: ${response.status}`);
      }
    } catch (error) {
      console.error('Error al subir el archivo:', error);
      if (error.code === 'ERR_NETWORK') {
        setError('No se pudo conectar con el servidor. Por favor verifica que el backend esté corriendo en http://127.0.0.1:3000');
      } else if (error.response) {
        setError(`Error del servidor: ${error.response.status} - ${error.response.data.message || 'Error desconocido'}`);
      } else {
        setError(error.message || 'Error al procesar el archivo');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="content">
        <img src="/images/KlikSymbol2.svg" alt="Klik Logo" className="App-logo" />
        <h1>Consulta los consumos de NEU</h1>
        <p className="subtitle">Solo debes compartirnos el listado de fronteras</p>
        <p className="subtitle">Y la fecha de consulta</p>
        
        <form onSubmit={handleSubmit}>
          <input 
            type="file" 
            id="file" 
            onChange={handleFileChange} 
            className="input-field file-input"
            accept=".xlsx,.xls"
          />
          <input 
            type="text" 
            id="email" 
            value={email} 
            onChange={handleEmailChange} 
            placeholder="A qué correo debe llegar el archivo resultado?"
            className="input-field"
          />
          <input 
            type="date" 
            id="date" 
            value={date} 
            onChange={handleDateChange} 
            className="input-field"
          />
          <button 
            type="submit" 
            className="submit-button" 
            disabled={loading}
          >
            {loading ? 'Procesando...' : '¡Consultar!'}
          </button>
        </form>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        {backendResponse && (
          <div className="response-info">
            <p>Archivo recibido: {backendResponse.fileName}</p>
            <p>Fecha recibida: {backendResponse.date}</p>
            <p>Email recibido: {backendResponse.email}</p>
          </div>
        )}
      </div>
      
      <footer className="footer">
        <p>Desarrollado por:</p>
        <img src="/images/klik-energy-logo-1.svg" alt="Klik Energy" className="footer-logo" />
      </footer>
    </div>
  );
}

export default App;