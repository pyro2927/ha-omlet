# Home Assistant Omlet Integration

This is a custom Home Assistant integration for the Omlet Smart Coop.

## Features

- Door control (open/close)
- Light control (on/off)
- Battery level monitoring
- Temperature and humidity monitoring
- Door state monitoring
- Light state monitoring

## Testing with Docker Compose

This repository includes a Docker Compose setup for testing the integration locally.

### Prerequisites

- Docker and Docker Compose installed on your system
- An Omlet API key (obtain from the Omlet app)

### Setup and Testing

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ha-omlet.git
   cd ha-omlet
   ```

2. Start the Home Assistant container:
   ```bash
   docker-compose up -d
   ```

3. Access Home Assistant at http://localhost:8123

4. Complete the initial Home Assistant setup

5. Go to Configuration > Integrations and click the "+" button

6. Search for "Omlet" and add your integration

7. Enter your Omlet API key when prompted

8. Select your Omlet device from the list

### Development Workflow

1. Make changes to the integration code in the `custom_components/omlet` directory

2. Restart the Home Assistant container to apply changes:
   ```bash
   docker-compose restart
   ```

3. Test your changes in the Home Assistant UI

### Stopping the Test Environment

When you're done testing, you can stop the container:
```bash
docker-compose down
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 