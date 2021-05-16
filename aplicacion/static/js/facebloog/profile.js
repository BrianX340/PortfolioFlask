window.onload = () => {

    recivir_profile()

}

function capitalize(string){
    string = string[0].toUpperCase() + string.slice(1);
    return string;
}

function get_photo(perfil_photo_dir){
    
    let entry = {
        'profilephoto': perfil_photo_dir
    };

    fetch(`${window.origin}/downloader`,
    {
        method: "GET",
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
            let imagen = data
            let img = document.getElementById('profile-image').innerHTML = data['coments']
            img.attr('src', URL.createObjectURL(imagen));
        })

    })
    .catch(function (error) {
        console.log("Fetch error: " + error);
        });



}






function recivir_profile() {


    let perfil_foto = ''
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
                document.getElementById('name').innerHTML = capitalize(data['name'])
                document.getElementById('lastname').innerHTML = capitalize(data['lastname'])
                document.getElementById('email').innerHTML = capitalize(data['email'])
                document.getElementById('cantpost').innerHTML = data['posts']
                document.getElementById('cantcoment').innerHTML = data['coments']
                if (data['profile_photo'] != ''){
                    perfil_photo_dir = data['profile_photo']
                }


        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
        });
        
        get_photo(perfil_photo_dir)
    

    })}