// Initialize and add the map
function initMap() {
  // The location of SJSU
  const sjsu = { lat: 37.335, lng: -121.881 };
  // The map, centered at SJSU
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: sjsu,
  });
  // create marker based on id_location (if updating, or if refreshing page)
    const loc = document.getElementById('id_location')
	console.log(loc);
  if (loc !== null && document.getElementById('id_location').value !== 'null') {
		console.log("in here");
	  coords = document.getElementById('id_location').value;
	console.log(coords);
  					var numArr = coords.split(',');
					const newLat = numArr[0].replace(/[^\d.-]/g, '');
					const newLong = numArr[1].replace(/[^\d.-]/g, '');
					console.log(newLat);
					console.log(newLong);
					const newPos = {lat: parseFloat(newLat), lng: parseFloat(newLong) }
  // The marker, positioned at SJSU
	map.setCenter(newPos);
	map.setZoom(12);
  const marker = new google.maps.Marker({
    position: newPos,
    map: map,
  });
  }
  const geocoder = new google.maps.Geocoder();
  
  try {
	document.getElementById("submit").addEventListener("click", () => {
    geocodeAddress(geocoder, map);
	});
  }
  catch(err){
	document.getElementById("search").addEventListener("click", () => {
    geocodeAndFind(geocoder, map);
  });
  }
}

function geocodeAndFind(geocoder, resultsMap) {
  const address = document.getElementById("address").value;
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
      resultsMap.setCenter(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
		var $j = jQuery.noConflict();
		console.log("Inside footer script");
		$.ajax({
		  url: '/send-coords/',
		  //data: {
			//'coords': { lat: 37.335, lng: -121.881 }
		  //},
		  dataType: 'json',
		  success: function (data) {
			  if (data) {
				  var stringified = JSON.stringify(data)
				  //alert(stringified);
				  const res = JSON.parse(stringified);
				  Object.entries(data).forEach((entry) => {
					const value = JSON.stringify(entry[1][0]);
					const pos = JSON.stringify(`${value}`)
					//console.log(pos);
					var numArr = pos.split(',');
					const newLat = numArr[0].replace(/[^\d.-]/g, '');
					const newLong = numArr[1].replace(/[^\d.-]/g, '');
					//console.log(newLat);
					//console.log(newLong);
					const newPos = {lat: parseFloat(newLat), lng: parseFloat(newLong) }
					new google.maps.Marker({
						map: resultsMap,
						position: newPos,
					});
					});
				  //for (var obj in object_arr) {
					  //var t = {lat: obj, lng: coord[1]};
					  //const res = JSON.parse(obj);
						//console.log(res);
				  //}
			  } 
		  } 
	  });
	 
  });
}

function geocodeAddress(geocoder, resultsMap) {
  const address = document.getElementById("address").value;
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
      resultsMap.setCenter(results[0].geometry.location);
	  resultsMap.setZoom(16);
      new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });
	  console.log(JSON.stringify(results[0].geometry.location));
	  
	  document.getElementById('id_location').value = JSON.stringify(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
