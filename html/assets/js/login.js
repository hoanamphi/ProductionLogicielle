$(document).ready(() => {
    $('#submit').click(() => {
        id = $('#id').val();
        mdp = $('#mdp').val();

        if (id != '' && mdp != '') {
            $.ajax({
                url: 'http://localhost:8080/api/login',
                type: 'POST',
                dataType: 'json',
                data: `id=${id}&mdp=${mdp}`,
        
                success: (json, status) => {
                    if (json == 'false')
                        alert('Mauvais identifiant / mot de passe.');
                    else alert('Base de données mise à jour!');
                },
        
                error: (result, status, error) => {
                    console.log(result)
                    console.log(status)
                    console.log(error)
                }
            });
        }
    })
})