
function recivir_profile() {



    let entry = {
        'user': 'ok'
    };

    fetch(`${window.origin}/consulta-profile`,
    {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
        .then(function (response) {

            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            response.json().then(function (data) {
                /*aca tomamos toda la informaciond del usuario y los introducimos en el document*/
                document.getElementById('name').innerHTML = data['name']
                document.getElementById('lastname').innerHTML = data['lastname']
                document.getElementById('email').innerHTML = data['email']
                document.getElementById('cantpost').innerHTML = data['posts']
                document.getElementById('cantcoment').innerHTML = data['coments']
            });

        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
    });

}

window.onload = () => {

    recivir_profile()

}