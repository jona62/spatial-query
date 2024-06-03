**Project Setup and Usage Guide**

**1. Setting Up MySQL Database**

From the root of your project, you can set up the MySQL database using Docker:

Run the following command to spin up the MySQL database along with PHPMyAdmin for graphical visualization:

```bash
docker-compose up -d
```

**2. Populating Database**

Navigate to the `scripts` directory:

```bash
cd scripts
```

To convert the CSV file to JSON format, run the `digest.sh` script with the path to the CSV file as an argument:

```bash
sh digest.sh ../data/McDonalds.csv
```

This script will convert the CSV file to JSON format.

**3. Populating the Database**

After converting the CSV file to JSON, you can populate the MySQL database with the data. Run the following command:

```bash
python3 populate-db.py
```
This Python script will populate the MySQL database with the data from the JSON file.

Using phpMyAdmin, you can visualize the database table at
http://localhost:8080/ with using name and password `Admin`
<img width="1506" alt="Screenshot 2024-06-03 at 2 35 39 AM" src="https://github.com/jona62/spatial-query/assets/25422400/9f9ded60-6ca7-42c9-b12b-d457519a6683">

**4. Starting the Flask Server**

Navigate to the `server` directory in a different tab:

```bash
cd spatial-query/server
```

Run the Flask application using the following command:

```bash
python3 app.py
```

This will start the Flask server on http://localhost:5001, making the API endpoints accessible.

**5. Setting Up the Web Interface**

Navigate to the `web` directory in a different tab:

```bash
cd spatial-query/web
```

First, install the dependencies using npm:

```bash
npm install
```

After installing the dependencies, build the JavaScript code:

```bash
npm run build
```

This will generate the JavaScript code needed for the web interface.

**6. Starting a Simple Web Server**

To serve the web interface, you can start a simple HTTP server using Python:

```bash
python3 -m http.server -d .
```

This starts a web server on http://localhost:8000/

This command will start a server in the current directory (`web`), allowing you to access the web interface in your browser.
![Screenshot 2024-06-03 at 1 57 17 PM](https://github.com/jona62/spatial-query/assets/25422400/436554eb-7426-45c0-b43e-ea763cf75e25)


**Note:** Make sure you have Docker, Python and npm installed on your system before running these commands.
