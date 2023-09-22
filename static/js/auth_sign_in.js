const BASE_URL = 'http://127.0.0.1:8000'

function SendLoginData(e) {
    e.preventDefault()
    var phone = document.getElementById('phone').value;
    var password = document.getElementById('password').value
    
    document.body.style.background = 'yellow';
    $.ajax(
        {
            url: BASE_URL + '/api/auth',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'phone': phone,
                'password': password
            }),
            success: (x) => console.log('SUCCESS'),
            error: (x) => console.log('1ERROR'),

        }
    )
}

$('#sign_in').on('click', SendLoginData)