# Home Assistant Omlet Integration

This is a custom integration for Home Assistant to control Omlet Smart Coops.

## Features

- Monitor battery level
- Control door state (open/close)
- Monitor light state and level
- Track last open/close times
- View door configuration settings

## Installation

### HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. In HACS, go to "Integrations"
3. Click the three dots in the top right and select "Custom repositories"
4. Add this repository URL: `https://github.com/pyro2927/ha-omlet`
5. Click "Add"
6. Find "Omlet" in the list and click "Install"
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/pyro2927/ha-omlet/releases)
2. Extract the `omlet` folder from the zip file
3. Copy the `omlet` folder to your Home Assistant `custom_components` directory
   - If the `custom_components` directory doesn't exist, create it
   - The path should be: `config/custom_components/omlet`
4. Restart Home Assistant

## Configuration

1. Go to Home Assistant Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Omlet"
4. Enter your Omlet API key
   - You can find your API key in the Omlet app under Settings > API
5. Click "Submit"

## Support

If you have any issues or questions, please [open an issue](https://github.com/pyro2927/ha-omlet/issues) on GitHub.

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