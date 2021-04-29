//var allMarkers = [];

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
  createBoxes(marker, map)
  //allMarkers.push(marker);
  }
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
  //console.log(allMarkers);
  // Create info boxes at all markers;
  //console.log(allMarkers);
}


function createBoxes(item, map, title, eventOwner, eventDate, eventPrice, eventMaxAge,
					eventMinAge, eventCapacity, eventActivityType, eventDescription, eventContactInfo) {
	const contentString =     '<div id="content">' +
    '<div id="siteNotice">' +
    "</div>" +
    '<h1 id="firstHeading" class="firstHeading">' + title + '</h1>' +
	'<h2 id="secondHeading" class="secondHeading">Hosted by:' + eventOwner + '</h2>' +
    '<div id="bodyContent">' +
    '<p><b>Date: </b>' + eventDate + '</p>' +
    '<p><b>Price: </b>' + eventPrice + '</p>' +
	'<p><b>Max Age: </b>' + eventMaxAge + '</p>' +
	'<p><b>Min Age: </b>' + eventMinAge + '</p>' +
	'<p><b>Capacity: </b>' + eventCapacity + '</p>' +
	'<p><b>Activity Type: </b>' + eventActivityType + '</p>' +
	'<p><b>Description: </b>' + eventDescription + '</p>' +
	'<p><b>Contact Info: </b>' + eventContactInfo + '</p>' +
    "</div>" +
    "</div>";
	//document.getElementById('firstHeading').innerHTML = title
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
				  var stringified = JSON.stringify(data);
				  console.log(stringified);
				  const res = JSON.parse(stringified);
				  Object.entries(data).forEach((entry) => {
					console.log(entry);
					const eventName = entry[1][1];
					console.log(eventName);
					const eventOwner = entry[1][2];
					console.log(eventOwner);
					const eventDate = entry[1][3];
					console.log(eventDate);
					const eventPrice = entry[1][4];
					console.log(eventPrice);
					const eventMaxAge = entry[1][5];
					console.log(eventMaxAge);
					const eventMinAge = entry[1][6];
					console.log(eventMinAge);
					const eventCapacity = entry[1][7];
					console.log(eventCapacity);
					const eventActivityType = entry[1][8];
					console.log(eventActivityType);
					const eventDescription = entry[1][9];
					console.log(eventDescription);
					const eventContactInfo = entry[1][10];
					console.log(eventContactInfo);
					const value = JSON.stringify(entry[1][0]);
					const pos = JSON.stringify(`${value}`)
					console.log(pos);
					var numArr = pos.split(',');
					const newLat = numArr[0].replace(/[^\d.-]/g, '');
					const newLong = numArr[1].replace(/[^\d.-]/g, '');
					//console.log(newLat);
					//console.log(newLong);
					const newPos = {lat: parseFloat(newLat), lng: parseFloat(newLong) }
					const marker = new google.maps.Marker({
						map: resultsMap,
						position: newPos,
					});
					
					createBoxes(marker, resultsMap, eventName, eventOwner, eventDate, eventPrice, eventMaxAge,
					eventMinAge, eventCapacity, eventActivityType, eventDescription, eventContactInfo)
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
      const marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });
	  //allMarkers.push(marker);
	  createBoxes(marker, resultsMap)
	  //console.log(JSON.stringify(results[0].geometry.location));
	  
	  document.getElementById('id_location').value = JSON.stringify(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
