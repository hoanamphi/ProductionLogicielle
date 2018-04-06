$(document).ready(() => {
    // Select updates
    $.ajax({
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=1`, // Disciplines

        success: (json, status) => {
            json.forEach(discipline => {
                $('#discipline_select').append(`<option value="${discipline}">${discipline}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });

    $.ajax({
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=1`, // Disciplines

        success: (json, status) => {
            json.forEach(discipline => {
                $('#discipline_select').append(`<option value="${discipline}">${discipline}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });

    $.ajax({ // Disciplines
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=1`,

        success: (json, status) => {
            json.forEach(discipline => {
                $('#discipline_select').append(`<option value="${discipline}">${discipline}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });
    $.ajax({ // Communes
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=0`,

        success: (json, status) => {
            json.forEach(commune => {
                $('#commune_select').append(`<option value="${commune}">${commune}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });
    $.ajax({ // Niveaux
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=2`,

        success: (json, status) => {
            json.forEach(niveau => {
                $('#niveau_select').append(`<option value="${niveau}">${niveau}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });
    $.ajax({ // Noms des installations
        url: 'http://localhost:8080/api/list',
        type: 'POST',
        dataType: 'json',
        data: `id=3`,

        success: (json, status) => {
            json.forEach(nom => {
                $('#nominstallation_select').append(`<option value="${nom}">${nom}</option>`);
            });
        },

        error: (result, status, error) => {
            console.log(result)
            console.log(status)
            console.log(error)
        }
    });

    // Search click
    $('#submit').click(() => {
        $('#results').remove();
        $('body').append(`
            <div id="results">   
                <div class="contact-clean" style="background-color:rgb(25,25,25);padding-top:20px;height:120px;padding-bottom:0;">
                    <div id="form" style="padding:20px;">
                        <h2 class="text-center" style="margin-bottom:0px;">Résultats de recherche</h2>
                        </div>
                </div>


                <div class="table-responsive" style="color:rgb(255,255,255);">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Installation</th>
                                    <th>Commune</th>
                                    <th>Code postal</th>
                                    <th>Lieu dit</th>
                                    <th>Voie</th>
                                    <th>Numéro de voie</th>
                                    <th>Wi-Fi</th>
                                    <th>Parking</th>
                                    <th>Desserte</th>
                                </tr>
                            </thead>
                            <tbody id="result-table"></tbody>
                        </table>
                    </div>
            </div>
        `);

        discipline = $('#discipline_select option:selected').val();
        commune = $('#commune_select option:selected').val();
        niveau = $('#niveau_select option:selected').val();
        desservissement = $('#desservissement_select option:selected').val();
        nominstallation = $('#nominstallation_select option:selected').val();

        discipline == undefined ? discipline = '':'';
        commune == undefined ? commune = '':'';
        niveau == undefined ? niveau = '':'';
        desservissement == undefined ? desservissement = '':'';
        nominstallation == undefined ? nominstallation = '':'';

        $.ajax({ // Noms des installations
            url: 'http://localhost:8080/api/search',
            type: 'POST',
            dataType: 'json',
            data: `discipline=${discipline}&commune=${commune}&niveau=${niveau}&desserte=${desservissement}&nom_installation=${nominstallation}`,
            
            success: (json, status) => {
                json.forEach(result => {
                    $('#result-table').append(`
                        <tr>
                            <th>${result[0] != null ? result[0] : ''}</th>
                            <th>${result[1] != null ? result[1] : ''}</th>
                            <th>${result[2] != null ? result[2] : ''}</th>
                            <th>${result[3] != null ? result[3] : ''}</th>
                            <th>${result[4] != null ? result[4] : ''}</th>
                            <th>${result[5] != null ? result[5] : ''}</th>
                            <th>${result[6] != null ? result[6] : ''}</th>
                            <th>${result[7] != null ? result[7] : ''}</th>
                            <th>${result[8] != null ? result[8] : ''}</th>
                        </tr>
                    `);
                });
            },

            error: (result, status, error) => {
                console.log(result)
                console.log(status)
                console.log(error)
            }
        });
    });
})