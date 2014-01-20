/**
 * Created by Lehel Kovach on 1/12/14.
 */

var propIndex = 0;

var propTypes = new Array();
propTypes[0] = ['Num', 'Number'];
propTypes[1] = ['TF', 'True/False'];
propTypes[2] = ['Str', 'Text'];
propTypes[3] = ['Date', 'Date & Time'];
propTypes[4] = ['Time', 'Time of Day'];
propTypes[5] = ['Dur', 'Time Duration'];
propTypes[6] = ['Url', 'URL'];
propTypes[7] = ['Geo', 'Location'];
propTypes[8] = ['Con', 'Topic'];


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
				'<input class=\'ctnewfeaturetitle\' value=\'' + title + '\' id=\'prop_' + propId +  '\' name=\'prop_' + propId + '\' />' +
                '<select class=\'ctnewtype\' id=\'proptype_' + propId + '\' name=\'proptype_' + propId + '\'>';


    for(i = 0; i < 9; i++) {
         rowHtml += '<option ';

         if(type == propTypes[i][0])
            rowHtml += ' selected ';

         rowHtml += 'value=\'' + propTypes[i][0] +  '\'>' + propTypes[i][1] + '</option>';
    }

    rowHtml += '</select>';


    if(isCategory != true) {
        rowHtml += '<input class=\'ctnewvalue\' value=\'' + val + '\' name=\'propval_' + propId + '\' id=\'propval_' + propId + '\' />'
    }

    rowHtml += '<button type=\'button\' id=\'remove' + propId + '\'>-</button></li>';


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

