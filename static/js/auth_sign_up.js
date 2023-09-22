const BASE_URL = 'http://127.0.0.1:8000'

function saveToken(data){
    console.log('token' + data)
    localStorage.setItem('access_token', JSON.stringify(data))
}

function handleUserData(data) {
    console.log(`${data.message}, ${data.HTTP_response}`)
    if (data.HTTP_response == 201){
        saveToken(data.token)
    }
}


function sendLoginData(e) {
    e.preventDefault()
    var phone = document.getElementById('phone').value;
    var password = document.getElementById('password').value
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value
    var email = document.getElementById('email').value;
    
    document.body.style.background = 'yellow';
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
            error: (x) => console.log('ERROR'),

        }
    )
}

$('#sign_up').on('click', sendLoginData)