const BASE_URL = 'http://127.0.0.1:8001'
const login_url = BASE_URL + '/auth/login'


function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
    }
} 

function logOut() {
    deleteAllCookies()
    window.location.replace('/auth/login')
}

function send_product() {
    var title = document.getElementById('title').value
    var description = document.getElementById('description').value;
    var amount = document.getElementById('amount').value
    var units = document.getElementById('unit_list').value;
    $.ajax(
        {
            url: BASE_URL + '/api/v1/add-product',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'title': title,
                'description': description,
                'amount': amount,
                'unit_id': units
            }),
            success: console.log('success'),
            error: (x) => console.log(`Error: ${x}`),
        }
    )
}
$('#add_product').on('click', send_product)
$('#logout').on('click', logOut)