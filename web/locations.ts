// Define the Location interface
interface Location {
    name: string;
    latitude: number;
    longitude: number;
    addressLine1: string;
    addressLine2: string;
    addressLine3: string;
    postcode: string;
    telephone: string;
    restaurantUrl: string;
    openstatus: string;
    hoursMonday: string;
    hoursTuesday: string;
    hoursWednesday: string;
    hoursThursday: string;
    hoursFriday: string;
    hoursSaturday?: string;
    hoursSunday?: string;
}

const map = L.map('map').setView([40, -100], 4);
let existingMarkers: L.Marker[] = [];

// Add a base tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

function getMcDonaldsWithinRange(latitude: number, longitude: number, range: number) {
    clearMarkers();
    fetch('http://localhost:5001/mickeyd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude,
            range: range
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`status: ${response.status} message: ${response.statusText}`);
        }
        return response.json() as Promise<Location[]>;
    })
    .then(data => {
        // Add markers for each McDonald's location from JSON data
        data.forEach(location => {
            const openStatusColor = location.openstatus === 'OPEN' ? 'green' : 'red';
            let tableContent = `
                <table>
                    <tr><th>Unique Id</th><td>${location.name}</td></tr>
                    <tr><th>Address</th><td>${location.addressLine1}, ${location.addressLine2}, ${location.addressLine3}</td></tr>
                    <tr><th>Postcode</th><td>${location.postcode}</td></tr>
                    <tr><th>Latitude</th><td>${location.latitude}</td></tr>
                    <tr><th>Longitude</th><td>${location.longitude}</td></tr>
                    <tr><th>Telephone</th><td>${location.telephone}</td></tr>
                    <tr><th>Restaurant URL</th><td><a href="${location.restaurantUrl}" target="_blank" rel="noopener noreferrer">${location.name}</a></td></tr>
                    <tr><th>Open Status</th><td style="color: ${openStatusColor};">${location.openstatus}</td></tr>
                    <tr><th>Monday</th><td>${location.hoursMonday}</td></tr>
                    <tr><th>Tuesday</th><td>${location.hoursTuesday}</td></tr>
                    <tr><th>Wednesday</th><td>${location.hoursWednesday}</td></tr>
                    <tr><th>Thursday</th><td>${location.hoursThursday}</td></tr>
                    <tr><th>Friday</th><td>${location.hoursFriday}</td></tr>
            `;

            if (location.hoursSaturday) {
                tableContent += `<tr><th>Saturday</th><td>${location.hoursSaturday}</td></tr>`;
            }
            if (location.hoursSunday) {
                tableContent += `<tr><th>Sunday</th><td>${location.hoursSunday}</td></tr>`;
            }

            tableContent += `</table>`;

            const marker = L.marker([location.latitude, location.longitude])
                .bindPopup(tableContent)
                .addTo(map);
            existingMarkers.push(marker);
        });
    })
    .catch(error => {
        console.error('Error retrieving McDonald\'s locations,', error);
    });
}

function clearMarkers() {
    existingMarkers.forEach(marker => {
        marker.remove(); // Remove each existing marker from the map
    });
    existingMarkers = []; // Clear the existingMarkers array
}
