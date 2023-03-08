// Handle the async company result calls to django backend
function reload_companies(number, id) {
    active_tab = id;
    $.ajax(
    {
        type:"GET",
        url: filter_search_url,
        data:{
            filter_number: number
        },
        success: function( data ) 
        {
            $(id).html(data);
        }
    })
}

function change_layout(number) {
    $.ajax(
    {
        type:"GET",
        url: layout_search_url,
        data:{
            layout_number: number
        },
        success: function( data ) 
        {
            $(active_tab).html(data);
            console.log("Success")
        }
    })
}
