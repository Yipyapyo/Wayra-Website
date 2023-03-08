// Handle the async company result calls to django backend
function reload_companies(number) {
    alert("called")
    $.ajax(
    {
        type:"GET",
        url: filter_search_url,
        data:{
            filter_number: number
        },
        success: function( data ) 
        {
            $('#all-companies').html(data);
            console.log("Success")
        }
    })
}
