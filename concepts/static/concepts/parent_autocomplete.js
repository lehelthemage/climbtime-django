/**
 * Created by Lehel Kovach on 1/23/14.
 */
$(document).ready(function() {
    $('.parent_autocomplete').autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: parentAutoUrl,
                    dataType: "jsonp",
                    data: {
                        term: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            $("#parent_id").val(item.id);
                            /*


                            getConceptProperties(propertiesAjaxUrl, item.id, isCategory);
*/
                            return {
                                label: item.title,
                                value: item.title,
                                id: item.id
                            }
                        }));
                    }
                });
            },
            minLength: 2,
            select: function(e, ui) {
                $("#parent_id").val(ui.item.id);
                getConceptProperties(propertiesAjaxUrl,ui.item.id, isCategory);
            }
        });

});