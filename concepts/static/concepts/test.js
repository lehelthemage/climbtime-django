/**
 * Created by dorian on 1/12/14.
 */
function hello() {
    alert('hello world');
}



//name: add_concept_action
//description: wordpress hook for when user submits a new concept via web form
/*
function add_concept_action() {

	//var feature_list = new Array();
	//use xpath to select all the feature boxes
	var featureTypes = jQuery("select[id*='feature_type']");
	var featureNames = jQuery("input[id*='feature_name']");
	var featureValues = jQuery("input[id*='feature_value']"); //input[@id="feature_value*"]

	var featureList = new Array();
	var feature;

	for(var i = 0; i != featureValues.length; i++) {
		feature = {
				type: featureTypes[i].value,
				name: featureNames[i].value,
				value: featureValues[i].value
		};
		featureList.push(feature);

	}

	var data = {
		action: 'addconcept',
		title: jQuery('#ct_title').val(),
		desc: jQuery('#ct_desc').val(),
		_featureList: featureList
	};


	//data = JSON.stringify(data);

	// since 2.8 ajaxurl is always defined in the admin header and points to admin-ajax.php
	jQuery.post(MyAjax.ajaxurl, data, function(response) {
		alert('Got this from the server: ' + response);
	});
}


function intialize_map() {
	intialized = true;

	var mapOptions = {
		center: new google.maps.LatLng(40.8688, 111.2195),
		zoom: 13,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	var map = new google.maps.Map(document.getElementById('geobox'), mapOptions);
	var defaultBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(30, 90),
		new google.maps.LatLng(50, 110)
		);

	map.fitBounds(defaultBounds);

	var input = (document.getElementById(value_id));
	var searchBox = new google.maps.places.SearchBox(input);

	//add removeListeners! for both places and map changed.
	google.maps.event.addListener(searchBox, 'places_changed', function() {
		var places = searchBox.getPlaces();

		for (var i = 0, marker; marker = markersArray[i]; i++) {
			marker.setMap(null);
		}

		markersArray = [];
		var bounds = new google.maps.LatLngBounds();

		for (var i = 0, place; place = places[i]; i++) {
			var image = {
			        url: place.icon,
			        size: new google.maps.Size(71, 71),
			        origin: new google.maps.Point(0, 0),
			        anchor: new google.maps.Point(17, 34),
			        scaledSize: new google.maps.Size(25, 25)
			};

			var marker = new google.maps.Marker({
		        map: map,
		        icon: image,
		        title: place.name,
		        position: place.geometry.location
			});

			markersArray.push(marker);
			google.maps.event.addListener(marker,"click",function(){});
			bounds.extend(place.geometry.location);
			map.fitBounds(bounds);

			if(i == 0) {
		    	alert(place.geometry.location + " asdf");
		    }
	    } //for (var i = 0, place; place = places[i]; i++)

	}); //google.maps.event.addListener

	google.maps.event.addListener(map, 'bounds_changed', function() {
		var bounds = map.getBounds();
	    searchBox.setBounds(bounds);
	});

	google.maps.event.addListener(map, 'click', function(e) {
		clearOverlays();

		var marker = new google.maps.Marker({
			map: map,
		    position: e.latLng
		});

		markersArray.push(marker);
		google.maps.event.addListener(marker,"click",function(){});
	});

}
*/

/*
jQuery('#geobox_bg').delay(400).fadeIn(300);

jQuery(this).clear();
jQuery(this).change(function() {

});

}
*/


/*

//needed globals
var initialized = false;
var currentPlace = null;
var markersArray = [];

jQuery(document).ready(function() {
	jQuery('#geobox_bg').hide();
	jQuery('#addconcept').click(function() { add_concept_action() });

  	jQuery('#add_feature').click(function() {


  		add_feature(null, null, null);

			//needed globals
			initialized = false;
			currentPlace = null;
			markersArray = [];

			function clearOverlays() {
				  for (var i = 0; i < markersArray.length; i++ ) {
				    markersArray[i].setMap(null);
				  }
				  markersArray = [];
			}



		});

		x++;
});


jQuery('#mapdone').click(function() {
	jQuery('#geobox_bg').delay(100).fadeOut(500);
});









*/