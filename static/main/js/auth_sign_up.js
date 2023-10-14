const BASE_URL = 'http://127.0.0.1:8001'

function saveToken(data){
    document.cookie=`access_token=${data.access_token}; path=/;`
    console.log(document.cookie)
}

function handleUserData(data) {
    console.log(`${data.message}`)
        saveToken(data.token)
        window.location.replace('/')
}


function sendLoginData(e) {
    e.preventDefault()
    var phone = document.getElementById('country_code').value + document.getElementById('phone').value;
    var password = document.getElementById('password').value
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value
    var email = document.getElementById('email').value;
    console.log(email + phone + first_name + last_name + password)
    $.ajax(
        {
            url: BASE_URL + '/api/auth/registration',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'phone': phone,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }),
            success: handleUserData,
            error: (x) => console.log(`ERROR: ${x}`),

        }
    )
}
console.log('wrtegwrseagfd')
$('#sign_up').on('click', sendLoginData)