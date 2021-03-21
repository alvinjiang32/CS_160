// Initialize and add the map
function initMap() {
  // The location of SJSU
  const sjsu = { lat: 37.335, lng: -121.881 };
  // The map, centered at SJSU
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: sjsu,
  });
  // The marker, positioned at SJSU
  const marker = new google.maps.Marker({
    position: sjsu,
    map: map,
  });
}
