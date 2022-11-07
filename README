# aws-ec2-monitor
This tools can be used to monitor a source or destination port for any network traffic and will shutdown the machine if no packets gets through the specified ports.

## Description
The scope of this project is to automatically shutdown an aws instance on itself if no network traffic is pressent. In the next phase this plugin will have the server client architecture along the current work flow for supporting kubernetes cluster.

## Getting Started

### Dependencies
* This application will work on linux platforms only and is being desgined for linux servers to reduce cost on the cloud environment.
* The build is tested in macOS and Linux machine only.

### Building
* python3 -m venv .venv
* . .venv/bin/activate
* pip install -r requirements.txt
* make
  
### Executing program
* After installing the '.whl' file using pip command you can run the following command to start the service.

```
 aws-monitor -s <SRC_PORT> -d <DEST_PORT> -l <LOGFILE> -t <TIME_IN_HRS>
 ```
 
* If no <SRC_PORT>/<DEST_PORT> are specified then by deafult all ports will be checked.
* The <LOGFILE> will have the request or response that was scanned by the application.
* The <TIME_IN_HRS> can be integer or float, eg value '1' is 1 hr and '1.5' is 1 hr and 30 min.

## Help
The application should be run with 'sudo' privilege if the user dose not have the super user privilege.

## Authors

👤 **Arun Thomas Alex**

- LinkedIn: [@arunthomasalex](https://in.linkedin.com/in/arun-alex)
- Github: [@arunthomasalex](https://github.com/arunthomasalex)

## Version History
* 1.0.0
    * Initial Release

## License
This project is licensed under the [BSD 2-Clause] License - see the LICENSE file for details.
