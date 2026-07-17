
const group = L.markerClusterGroup();

fetch(`/loadnotsavedspots?lat=${lat}&lng=${lng}&stuff=${stuff}`)
    .then(response => response.json())
    .then(places => {
        for (const place of places){
        
            var marker = L.marker([place["lat"],place["lng"]]).bindPopup(place.name+ " :D");
            group.addLayer(marker);
        }
        map.addLayer(group);
    });

