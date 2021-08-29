function confirm_delete(url, id) {
    swal({
        title: "¿Desea continuar?",
        text: "Una vez eliminado el registro no se recuperará",
        type: 'warning',
        buttonsStyling: false,
        confirmButtonClass: 'btn btn-lg btn-danger m-1',
        cancelButtonClass: 'btn btn-lg btn-danger m-1',
        showCancelButton: true,
        confirmButtonText: "Sí, borrar",
        cancelButtonText: "Cancelar",
    })
    .then(result => {        
        if (result) {
            $.ajaxSetup({
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            $.ajax({
                url: url,
                data: {id: id},
                type: "delete",
                dataType: "json",
                success: function (response) {
                    if ( response.status ) {
                        $(".table").DataTable().row($('.table tr[data-id="' + id + '"]')).remove().draw();
                    }
                    
                    swal({
                        text: response.text,
                        type: response.type,
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-lg btn-danger',
                    });                                        
                },
                error: function (data) {
                    console.log(data);
                },
            });
        }
    });
}