const BASE_URL = 'http://127.0.0.1:8001'
const login_url = BASE_URL + '/auth/login'

// async function fetchWithAuth(url_login) {
//     const access_token = JSON.parse(localStorage.getItem('access_token'))
//     let current_time = new Date()
//     current_time = Date.now() + current_time.getTimezoneOffset() * 60000
//     console.log(current_time)
//     try {
//         console.log(access_token.expire_in * 1000)
//         if (access_token != null && access_token.expire_in * 1000 > current_time) {
//             $.ajax(
//                 {
//                     url: BASE_URL + '/api/auth/token',
//                     method: 'post',
//                     dataType: 'json',
//                     contentType: 'application/json',
//                     data: JSON.stringify({
//                         'access_token': access_token.access_token,
//                     }),
//                     success: userUnautharized,
//                     error: (x) => console.log('ERROR'),
        
//                 }
//             )
//         } else {
//             localStorage.removeItem('access_token')
//             return window.location.replace(url_login)
//         }
//     } catch {return window.location.replace(url_login)}
// }

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
    console.log(units)
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
console.log(1231232)
$('#add_product').on('click', send_product)
// var toastElList = [].slice.call(document.querySelectorAll('.toast'))
// var toastList = toastElList.map(function (toastEl) {
//   return new bootstrap.Toast(toastEl, 'show')
// })
$('#logout').on('click', logOut)