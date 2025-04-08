# NEU API

API para la gestión de datos de consumo de energía y envío de correos electrónicos.

## Estructura del Proyecto

```
NEU_API/
├── backend/           # Servidor Flask
│   ├── app.py        # Aplicación principal
│   └── requirements.txt
└── frontend/         # Cliente React
    ├── package.json
    └── src/          # Código fuente React
```

## Requisitos

### Backend
- Python 3.9+
- Flask
- pandas
- yagmail
- flask-cors

### Frontend
- Node.js
- React
- Axios

## Configuración

1. Backend:
```bash
cd backend
python -m venv NEU
source NEU/bin/activate  # En Unix/MacOS
pip install -r requirements.txt
```

2. Frontend:
```bash
cd frontend
npm install
```

## Ejecución

1. Backend:
```bash
cd backend
python app.py
# El servidor se iniciará en http://127.0.0.1:3000
```

2. Frontend:
```bash
cd frontend
npm start
# La aplicación se iniciará en http://localhost:3001
```

## Funcionalidades

- Carga de archivos Excel
- Procesamiento de datos de consumo de energía
- Envío de correos electrónicos con archivos adjuntos
- Interfaz de usuario intuitiva

## Endpoints API

- `GET /`: Ruta de prueba
- `POST /upload`: Carga y procesamiento de archivos
- `POST /send-email`: Envío de correos electrónicos

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request 