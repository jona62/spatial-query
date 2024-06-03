"use strict";
var map = L.map('map').setView([40, -100], 4);
var existingMarkers = [];
// Add a base tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);
function getMcDonaldsWithinRange(latitude, longitude, range) {
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
        .then(function (response) {
        if (!response.ok) {
            throw new Error("status: ".concat(response.status, " message: ").concat(response.statusText));
        }
        return response.json();
    })
        .then(function (data) {
        // Add markers for each McDonald's location from JSON data
        data.forEach(function (location) {
            var openStatusColor = location.openstatus === 'OPEN' ? 'green' : 'red';
            var tableContent = "\n                <table>\n                    <tr><th>Unique Id</th><td>".concat(location.name, "</td></tr>\n                    <tr><th>Address</th><td>").concat(location.addressLine1, ", ").concat(location.addressLine2, ", ").concat(location.addressLine3, "</td></tr>\n                    <tr><th>Postcode</th><td>").concat(location.postcode, "</td></tr>\n                    <tr><th>Latitude</th><td>").concat(location.latitude, "</td></tr>\n                    <tr><th>Longitude</th><td>").concat(location.longitude, "</td></tr>\n                    <tr><th>Telephone</th><td>").concat(location.telephone, "</td></tr>\n                    <tr><th>Restaurant URL</th><td><a href=\"").concat(location.restaurantUrl, "\" target=\"_blank\" rel=\"noopener noreferrer\">").concat(location.name, "</a></td></tr>\n                    <tr><th>Open Status</th><td style=\"color: ").concat(openStatusColor, ";\">").concat(location.openstatus, "</td></tr>\n                    <tr><th>Monday</th><td>").concat(location.hoursMonday, "</td></tr>\n                    <tr><th>Tuesday</th><td>").concat(location.hoursTuesday, "</td></tr>\n                    <tr><th>Wednesday</th><td>").concat(location.hoursWednesday, "</td></tr>\n                    <tr><th>Thursday</th><td>").concat(location.hoursThursday, "</td></tr>\n                    <tr><th>Friday</th><td>").concat(location.hoursFriday, "</td></tr>\n            ");
            if (location.hoursSaturday) {
                tableContent += "<tr><th>Saturday</th><td>".concat(location.hoursSaturday, "</td></tr>");
            }
            if (location.hoursSunday) {
                tableContent += "<tr><th>Sunday</th><td>".concat(location.hoursSunday, "</td></tr>");
            }
            tableContent += "</table>";
            var marker = L.marker([location.latitude, location.longitude])
                .bindPopup(tableContent)
                .addTo(map);
            existingMarkers.push(marker);
        });
    })
        .catch(function (error) {
        console.error('Error retrieving McDonald\'s locations,', error);
    });
}
function clearMarkers() {
    existingMarkers.forEach(function (marker) {
        marker.remove(); // Remove each existing marker from the map
    });
    existingMarkers = []; // Clear the existingMarkers array
}
