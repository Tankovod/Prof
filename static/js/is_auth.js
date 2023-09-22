const BASE_URL = 'http://127.0.0.1:8000'
const login_url = BASE_URL + '/auth/login'

async function fetchWithAuth(url_login) {
    const access_token = JSON.parse(localStorage.getItem('access_token'))
    let current_time = new Date()
    current_time = Date.now() + current_time.getTimezoneOffset() * 60000
    console.log(current_time)
    try {
        console.log(access_token.expire_in * 1000)
        if (access_token != null && access_token.expire_in * 1000 > current_time) {
            $.ajax(
                {
                    url: BASE_URL + '/api/auth/token',
                    method: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'access_token': access_token.access_token,
                    }),
                    success: userUnautharized,
                    error: (x) => console.log('ERROR'),
        
                }
            )
        } else {
            localStorage.removeItem('access_token')
            return window.location.replace(url_login)
        }
    } catch {return window.location.replace(url_login)}
}


function userUnautharized(exceprion) {
    if (exceprion == 401) {
        return window.location.replace(login_url)
    }
}

fetchWithAuth(login_url)

