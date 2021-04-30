var allMarkers = [];

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
  if (loc !== null && document.getElementById('id_location').value !== 'null') {
		//console.log("in here");
	  coords = document.getElementById('id_location').value;
	//console.log(coords);
  					var numArr = coords.split(',');
					const newLat = numArr[0].replace(/[^\d.-]/g, '');
					const newLong = numArr[1].replace(/[^\d.-]/g, '');
					//console.log(newLat);
					//console.log(newLong);
					const newPos = {lat: parseFloat(newLat), lng: parseFloat(newLong) }
  // The marker, positioned at SJSU
	map.setCenter(newPos);
	map.setZoom(12);
  const marker = new google.maps.Marker({
    position: newPos,
    map: map,
  });
  }
  allMarkers.push(marker);
  const geocoder = new google.maps.Geocoder();
  //console.log("Inside boxes");
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
  //console.log("Inside boxes");
  console.log(allMarkers);
  // Create info boxes at all markers
  allMarkers.forEach(createBoxes, map);
  //console.log(allMarkers);
}


function createBoxes(item, map) {
	const contentString =     '<div id="content">' +
    '<div id="siteNotice">' +
    "</div>" +
    '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
    '<div id="bodyContent">' +
    "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
    "sandstone rock formation in the southern part of the " +
    "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) " +
    "south west of the nearest large town, Alice Springs; 450&#160;km " +
    "(280&#160;mi) by road. Kata Tjuta and Uluru are the two major " +
    "features of the Uluru - Kata Tjuta National Park. Uluru is " +
    "sacred to the Pitjantjatjara and Yankunytjatjara, the " +
    "Aboriginal people of the area. It has many springs, waterholes, " +
    "rock caves and ancient paintings. Uluru is listed as a World " +
    "Heritage Site.</p>" +
    '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">' +
    "https://en.wikipedia.org/w/index.php?title=Uluru</a> " +
    "(last visited June 22, 2009).</p>" +
    "</div>" +
    "</div>";
	const infowindow = new google.maps.InfoWindow({
		content: contentString,
	});
	item.addListener("click", () => {infowindow.open(map, item); });
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
		//console.log("Inside footer script");
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
	  //console.log(JSON.stringify(results[0].geometry.location));
	  
	  document.getElementById('id_location').value = JSON.stringify(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
