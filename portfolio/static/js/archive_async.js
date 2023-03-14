// Handle the async company result calls to django backend
function reload_archived_companies(number) {
    alert('called');
    $.ajax(
    {
        type:"GET",
        url: filter_companies_url,
        data:{
            filter_number: number
        },
        success: function( data ) 
        {
            $(".companies-table").html(data);
            alert('success');
        }
    })
}