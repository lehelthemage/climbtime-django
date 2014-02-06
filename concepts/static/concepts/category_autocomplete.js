/**
 * Created by Lehel Kovach on 1/23/14.
 */
$(document).ready(function() {
    $('.category_autocomplete').autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: categoryAutoUrl,
                    dataType: "jsonp",
                    data: {
                        term: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            $("#category_id").val(item.id);

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
                getConceptProperties(propertiesAjaxUrl,ui.item.id, false);
            }
        });

});/**
 * Created by Dorian on 2/3/14.
 */
