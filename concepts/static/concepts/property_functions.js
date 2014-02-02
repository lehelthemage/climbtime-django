/**
 * Created by Lehel Kovach on 1/12/14.
 */

var propIndex = 0;

var propTypes = {
    'Num': 'Number',
    'TF': 'True/False',
    'Str': 'Text',
    'Date': 'Date & Time',
    'Days': 'Day(s) of Week',
    'Time': 'Time of Day',
    'Dur':  'Time Duration',
    'Url': 'URL',
    'Geo': 'Location',
    'Con': 'Topic'
}

function addPropertyRow(title, type, val, propId, isCategory) {

    propIndex++;

    if(title == null) {
        title = '';
        type = '';
        val = '';
        propId = null;
    }

    if(propId == null)
        propId = propIndex;



	rowHtml = '<li id=\'proprow_' + propId + '\'>' +
                '<div class=\'property_row\'>' +
				'<input class=\'ctnewfeaturetitle\' value=\'' + title + '\' id=\'prop_' + propId +  '\' name=\'prop_' + propId + '\' />' +
                '<select class=\'ctnewtype\' id=\'proptype_' + propId + '\' name=\'proptype_' + propId + '\'>';


    for(var i in propTypes) {
        rowHtml += '<option ';

         if(type == i)
            rowHtml += ' selected ';

         rowHtml += 'value=\'' + i +  '\'>' + propTypes[i] + '</option>';
    }

    rowHtml += '</select>';


    if(isCategory != true) {
        rowHtml += '<input class=\'ctnewvalue\' value=\'' + val + '\' name=\'propval_' + propId + '\' id=\'propval_' + propId + '\' />'
    }

    rowHtml += '<button class=\'ctbutton remove-button\' type=\'button\' id=\'remove' + propId + '\'>-</button></div></li>';


    jQuery('#prop_list').append(rowHtml);


    jQuery('#remove' + propId).click(function() {
		var currentId = $(this).attr('id');
        var y = currentId.substring(8);
        jQuery('#proprow_' + propId).remove();
	});

	jQuery("#feature_type" + propId).change(function() {
			var numSuffix = jQuery(this).attr('id').substring(12);
			jQuery('#feature_value' + numSuffix).unbind();

			jQuery('#feature_value' + numSuffix).click(function() {
				//get the text of the selected value
				var numSuffix = jQuery(this).attr('id').substring(13);
				var selectVal = jQuery('#feature_type' + numSuffix + ' option:selected').val();
				var value_id = jQuery(this).attr('id');

				var position = jQuery(this).position();
				$('#geobox_bg').css("position", "absolute");
				$('#geobox_bg').css("left", position.left + 100);
				$('#geobox_bg').css("top", position.top);


				if(selectVal == 'Location') {
					if(!initialized) {


					}
					else {
						jQuery('#geobox_bg').hide();
					}

				}

			});  //jQuery('#feature_value' + numSuffix).click
		});

}

function getConceptProperties(url, categoryId, forCategory) {

    url = url + categoryId;

    $.ajax({
        url: url,
        dataType: "jsonp",
        data: {
            category_id: categoryId
        },
        success: function (data) {
            $.each(data, function(index, element) {
                addPropertyRow(element.title, element.property_type, null, null, forCategory);
            });
        }
    });
}

