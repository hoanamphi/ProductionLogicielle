$(document).ready(() => {
    $('#submit').click(() => {
        $.ajax({
            url: 'localhost:8080/api/list',
            type: 'GET',
            dataType: 'json',
            data: `id=0`, // Communes

            success: (json, status) => {
                console.log(json);
                response(json.map(e => {
                    return 
                }));
            },

            error: (result, status, error) => {
                console.log(result)
                console.log(status)
                console.log(error)
            }
        });
    });
})