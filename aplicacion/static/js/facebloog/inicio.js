function submit_post(e) {
    let posteo = document.getElementById("queestaspensando");
    let message = posteo.textContent;
    let entry = {
        message: message
    };
    fetch(`${window.origin}/crear-facebloogpost`, {
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
                console.log(data);
            });
        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
        });
    /*aca limpiamos el campo*/
    posteo.innerText = ''
}

function submit_commentario(e) {
    /*id del post*/
    let idpost = e.path[0].getAttribute('id')
    /*seleccionamos el post*/
    let posteo = document.getElementById(idpost.toString());
    /*comentario a postear*/
    let texto = posteo.innerText;
    let entry = {
        'idpost': idpost,
        'texto': texto
    };

    fetch(`${window.origin}/crear-facebloogcomments`, {
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

                console.log(data);
            });
        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
        });

    /*aca limpiamos el campo*/
    posteo.innerText = ''

}


function recivir_post() {



    let entry = {
        'post': 'data_comment'
    };

    fetch(`${window.origin}/consulta-posteos`,
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
                /*aca recivimos los post con el siguente formato*/
                /*
                {
                    postid:{
                        'commentid': {
                            'content': contenido,
                            'user_comented': user
                        },

                    }
                }
                */
               document.getElementById('bloques').innerHTML = data['bloque']

            });

        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
    });

}





window.onload = () => {
    recivir_post()
    document.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
            mensajetipo = e.path[0].getAttribute('mensajetipo')

            /* Aca separamos por tipo de mensaje */
            if (mensajetipo == 'posteo') {
                submit_post(e)
            } else if (mensajetipo == 'comentario') {
                submit_commentario(e)
            }
            recivir_post()
        }
    })
}

